# TMC enable chip
EN_PIN = 21

# TMC motor control pins
STEP_PIN = 22
DIR_PIN = 23

# TMC UART comminication
UART_TX_PIN = 18
UART_RX_PIN = 19

# NEMA 17 motor parametrs
STEPS_PER_REV = 400
MICROSTEPS = 8
DIRECTION = "right"
STEP_DELAY = 172410
SPEED = 1000
FINAL_SPEED = round(STEP_DELAY / SPEED)