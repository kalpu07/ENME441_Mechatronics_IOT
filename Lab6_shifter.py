import RPi.GPIO as GPIO
import time

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
dataPin, latchPin, clockPin = 23, 24, 25
GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial=0)
GPIO.setup(clockPin, GPIO.OUT, initial=0)

# --- Helper function to pulse a pin ---
def ping(pin):
    GPIO.output(pin, 1)
    time.sleep(0.00001)  # short delay
    GPIO.output(pin, 0)

# --- Function to shift a byte ---
def shiftByte(byte):
    GPIO.output(latchPin, 0)  # latch low while sending
    for i in range(8):        # LSB first
        GPIO.output(dataPin, byte & (1 << i))
        ping(clockPin)
    GPIO.output(latchPin, 1)  # latch high to update LEDs
    GPIO.output(latchPin, 0)

# --- Main loop: turn on LEDs one by one ---
try:
    while True:
        for i in range(8):
            byte = 1 << i  # only one LED on at a time
            shiftByte(byte)
            print(f"LED {i + 1} on")
            time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
