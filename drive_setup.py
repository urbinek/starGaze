import machine
import utime
import global_parm 

# Define pins for TMC2208 driver
en_pin = machine.Pin(global_parm.EN_PIN, machine.Pin.OUT)
step_pin = machine.Pin(global_parm.STEP_PIN, machine.Pin.OUT)
dir_pin = machine.Pin(global_parm.DIR_PIN, machine.Pin.OUT)

# Define UART parameters
uart = machine.UART(1, baudrate=115200, tx=global_parm.UART_TX_PIN, rx=global_parm.UART_RX_PIN)

def run():
    # Enable TMC2208
    en_pin.value(0)

    print(f"Motor parameters:")
    print(f"- initial mikrosteps : {global_parm.STEPS_PER_REV * global_parm.MICROSTEPS}/360deg")
    print(f"- initial step interval: {global_parm.FINAL_SPEED}us")

    while True:
        dir()
        step()                                      # Step in one direction
        utime.sleep_us(global_parm.FINAL_SPEED)     # Add a delay to control speed
  

def step():
    step_pin.value(1)
    utime.sleep_us(1)
    step_pin.value(0)
    utime.sleep_us(1)

def dir():
    if global_parm.DIRECTION == "right":
        dir_pin.value(0)
    else:
        dir_pin.value(1)

