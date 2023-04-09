import machine
import utime
import global_parm 

# Define pins for TMC2208 driver
en_pin = machine.Pin(global_parm.EN_PIN, machine.Pin.OUT)
step_pin = machine.Pin(global_parm.STEP_PIN, machine.Pin.OUT)
dir_pin = machine.Pin(global_parm.DIR_PIN, machine.Pin.OUT)

# Define UART parameters
uart = machine.UART(1, baudrate=115200, tx=global_parm.UART_TX_PIN, rx=global_parm.UART_RX_PIN)

def setup():
    # Enable TMC2208
    en_pin.value(0)

    # Set TMC2208 base parameters
    reset_tmc2208()
    tmc2208_set_current()
    tmc2208_set_microstep_setting(microstep=256)
    global_parm.MICROSTEPS = tmc2208_read_microstep_setting()

    print(f"Motor parameters:")
    print(f"- initial mikrosteps : {global_parm.STEPS_PER_REV * global_parm.MICROSTEPS}/360deg")
    print(f"- initial step interval: {global_parm.FINAL_SPEED}us")


def reset_tmc2208():
    # Reset GCONF register to default value (0x00000000)
    uart.write(b'\x05\x00\x00\x00')         # Send GCONF register write command via UART
    utime.sleep_ms(100)

    # Reset IHOLD_IRUN register to default value (0x00000000)
    uart.write(b'\x10\x00\x00\x00')         # Send IHOLD_IRUN register write command via UART
    utime.sleep_ms(100)

    # Reset CHOPCONF register to default value (0x00010000)
    uart.write(b'\x6C\x00\x01\x00\x00')     # Send CHOPCONF register write command via UART
    utime.sleep_ms(100)

def tmc2208_set_current():
    # Set current level (A) to 1.68A
    current = 0b1000000010101010   # Set current to 1.68A
    uart.write(b'\x01\x00' + current.to_bytes(2, 'big'))  # Send IHOLD_IRUN register write command via UART
    utime.sleep_ms(100)
    
    # Confirm that the current limit has been set correctly
    uart.write(b'\x91\x00')   # Send IHOLD_IRUN register read command via UART
    utime.sleep_ms(100)
    response = uart.read()
    current_reg = int.from_bytes(response[2:], 'big')
    if current_reg != current:
        print("Current limit was not set correctly!")


def tmc2208_set_microstep_setting(microstep=256):
    # Send GCONF register write command via UART
    uart.write(b'\x05\x00\x00\x03')

    # Select microstep mode based on input parameter
    if microstep == 256:    uart.write(b'\x00\x00\x00\x08')
    elif microstep == 128:  uart.write(b'\x00\x00\x00\x07')
    elif microstep == 64:   uart.write(b'\x00\x00\x00\x06')
    elif microstep == 32:   uart.write(b'\x00\x00\x00\x05')
    elif microstep == 16:   uart.write(b'\x00\x00\x00\x04')
    elif microstep == 8:    uart.write(b'\x00\x00\x00\x03')
    elif microstep == 4:    uart.write(b'\x00\x00\x00\x02')
    elif microstep == 2:    uart.write(b'\x00\x00\x00\x01')
    else:                   uart.write(b'\x00\x00\x00\x08') # Default to microstep 1/256 step
    # Wait for command to complete
    utime.sleep_ms(100)

def tmc2208_read_microstep_setting():
    # Request the contents of the CHOPCONF register (0x6C) with the read bit set (0x80)
    uart.write(b'\xEC\x00')                 # Send the read request
    utime.sleep_ms(100)
    response = uart.read(4)                 # Read the 4-byte response

    value = int.from_bytes(response, 'big') # Convert response bytes to a 32-bit integer
    mres = (value >> 24) & 0x07             # Extract the MRES bits (bits 24 to 26) and calculate the microstep setting
    microsteps = 2 ** mres                  # Calculate the number of microsteps
    
    return microsteps

