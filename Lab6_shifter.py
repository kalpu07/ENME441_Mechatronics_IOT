import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# ------------------------Shifter Class-----------------------------------------
class Shifter:
    
    #INIT method runs evertime a new object is created 
    def __init__(self, serial_pin, clock_pin, latch_pin):
        # Assigning values to attributes
        self.serialPin = serial_pin
        self.clockPin = clock_pin  
        self.latchPin = latch_pin

        # Setting up GPIO pins
        GPIO.setup(self.serialPin, GPIO.OUT)
        GPIO.setup(self.latchPin, GPIO.OUT, initial=0)
        GPIO.setup(self.clockPin, GPIO.OUT, initial=0)

    # method that pings either clock or latch pin
    def __ping(self, pin):
        GPIO.output(pin, 1)
        time.sleep(0)
        GPIO.output(pin, 0)

    # sends bytpe of data to output
    def shiftByte(self, data_byte):
        for i in range(8):
            GPIO.output(self.serialPin, data_byte & (1 << i))
            self.__ping(self.clockPin)  # add bit to register
        self.__ping(self.latchPin)  # send register to output

    try:
        shifter = Shifter(23, 25, 24)  # data, clock, latch pins
        while True:
            for i in range(2**8):
                shifter.shiftByte(i)
                time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()