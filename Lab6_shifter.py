import RPi.GPIO as GPIO
import time
import random

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

# ------------------------Bug Class-----------------------------------------
class Bug:
    
    def __init__(self, serial_pin, clock_pin, latch_pin, timestep=0.1, x=3, isWrapOn=False):
        # Set attributes with default values
        self.timestep = timestep
        self.x = x
        self.isWrapOn = isWrapOn
        
        # Private shifter object
        self.__shifter = Shifter(serial_pin, clock_pin, latch_pin)
        
        # Track if bug is moving
        self.is_moving = False
        
        # Show starting position
        self.__shifter.shiftByte(1 << self.x)

    def start(self):
        """Start the bug moving"""
        self.is_moving = True

    def stop(self):
        """Stop the bug and turn off LED"""
        self.is_moving = False
        self.__shifter.shiftByte(0)

    def move(self):
        """Move the bug one step - call this repeatedly"""
        if not self.is_moving:
            return
            
        # Random step: left or right
        step = random.choice([-1, 1])
        new_x = self.x + step
        
        # Handle movement based on wrap mode
        if self.isWrapOn:
            # Wrap around edges
            self.x = new_x % 8
        else:
            # Bounce off edges
            if 0 <= new_x <= 7:
                self.x = new_x
        
        # Update LED display
        self.__shifter.shiftByte(1 << self.x)