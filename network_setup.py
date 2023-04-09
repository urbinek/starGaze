import network
import ujson

# Load the settings.json file
with open('settings.json', 'r') as settings:
    setup = ujson.load(settings)

# Extract the network details from the setup dictionary
ssid = setup['network']['ssid']
password = setup['network']['password']

# Connect to the WiFi network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Wait until the device is connected to the WiFi network
while not wlan.isconnected():
    pass

# Print the device's IP address
print("Device connected to WiFi network")
print("IP address:", wlan.ifconfig()[0])
