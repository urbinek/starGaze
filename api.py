import _thread
import usocket
import ujson
import global_parm 

print("Starting starGaze program!")


# Thread function
import drive_setup
def loop():
    drive_setup.run()

# Start the loop in a separate thread
_thread.start_new_thread(loop, ())

def parse_headers(cl_file):
    headers = {}
    while True:
        line = cl_file.readline().decode('utf-8').strip()
        if not line:
            break

        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()

    return headers

# Function to handle incoming POST requests
def handle_post_request(request, cl_file):
    try:
        payload = ujson.loads(request)

        if 'dir' in payload:
            global_parm.DIRECTION = payload['dir']
        if 'speed' in payload:
            global_parm.SPEED = int(payload['speed'])
        
        global_parm.FINAL_SPEED = round(global_parm.STEP_DELAY / global_parm.SPEED)
        response_data = {
            "status": "success",
            "dir": global_parm.DIRECTION,
            "speed": global_parm.SPEED,
            "delay": global_parm.FINAL_SPEED
        }

        response_body = ujson.dumps(response_data)
        response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + response_body
    except Exception as e:
        print("Error:", e)
        response = "HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\n\r\n{\"error\": \"Invalid JSON\"}"
    
    cl_file.write(response)


# Main function to create the REST API server
def main():
    with open('settings.json', 'r') as settings:
        setup = ujson.load(settings)

    addr = usocket.getaddrinfo('0.0.0.0', setup['starGaze']['api_port'])[0][-1]

    socket = usocket.socket()
    socket.bind(addr)
    socket.listen(1)

    print("Listening on http://{}:{}".format(*addr))

    while True:
        cl, addr = socket.accept()
        print("Client connected from:", addr)

        cl_file = cl.makefile('rwb', 0)
        request_line = cl_file.readline().decode('utf-8')
        method, path, _ = request_line.split()

        if method == 'POST' and path == '/api/v1':
            headers = parse_headers(cl_file)
            content_length = int(headers.get('Content-Length', 0))
            request = cl_file.read(content_length)
            print(f"Request from client: {ujson.loads(request)}")
            handle_post_request(request, cl_file)
        else:
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nNot Found"
            cl_file.write(response)
            cl_file.flush()

        cl.close()

# Start the REST API server
main()
