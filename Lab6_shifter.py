#Kalp Upadhayay
#ENME441 - Lab 6 Shift Registers

#Shifter and Bug Classes

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
        GPIO.setup(self.latchPin, GPIO.OUT, initial = 0)
        GPIO.setup(self.clockPin, GPIO.OUT, initial = 0)

    # Private method that pings either clock or latch pin
    def __ping(self, pin):
        GPIO.output(pin, 1) #Turning on
        time.sleep(0)
        GPIO.output(pin, 0) #Turning Off

    # sends bytpe of data to output
    def shiftByte(self, data_byte):

        GPIO.output(self.latchPin, GPIO.LOW)
        for i in range(8):
            GPIO.output(self.serialPin, GPIO.LOW)  # Clear all bits
            self.__ping(self.clockPin)
        GPIO.output(self.latchPin, GPIO.HIGH)

        GPIO.output(self.latchPin, GPIO.LOW)

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

    #Just starts the bug moving - turns the flag to true
    def start(self):
        self.is_moving = True
        print("Bug started moving")

    #Stop the bug turn off LED
    def stop(self):
        self.is_moving = False
        self.__shifter.shiftByte(0)
        print("Bug stopped, and LED is OFF")

    # Moving the bug one step
    def move(self):

        #Checks to see if bug is moving if not it exits
        if self.is_moving == False:
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