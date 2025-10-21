# Kalp Upadhayay
# Lab 6 - Shifter and Bug Class File

import RPi.GPIO as GPIO
import time
import random 

GPIO.setmode(GPIO.BCM)

#Implementing the Shifter Class

class Shifter:

    #Runs everytime a shifter is created
    def __init__(self, serial_pin, clock_pin, latch_pin):

        #Assigning passed values to class attributes
        self.serialPin = serial_pin
        self.clockPin = clock_pin
        self.latchPin = latch_pin

        #----GPIO Configeration -----Setting all three to low
        GPIO.setup(self.serialPin, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.clockPin, GPIO.OUT, initial = GPIO.LOW)
        GPIO.setup(self.latchPin, GPIO.OUT, initial = GPIO.LOW)

    #Clocks one bit into the shift register
    def _ping(self):

        GPIO.output(self.clockPin, GPIO.HIGH)
        GPIO.output(self.clockPin, GPIO.LOW)

    def shiftByte(self, data_byte):

        GPIO.output(self.latchPin, GPIO.LOW)

        #Looping bit by bit
        for i in range(8):

            #Checking the most significant bit
            if data_byte & 0x80:
                #If but is 1, its HIGH
                GPIO.output(self.serialPin, GPIO.HIGH)
            else:
                #In this its 0 so its set to low
                GPIO.output(self.serialPin, GPIO.LOW)

            #Clocks the single bit into the register
            self._ping()

            #Shifting the data one positions left for the next increment
            data_byte = data_byte << 1

        GPIO.output(self.latchPin, GPIO.HIGH)

    # FIX: Added all_off method for completeness
    def all_off(self):
        """Turns off all 8 LEDs by shifting a byte of zeros."""
        self.shiftByte(0x00)

class Bug:

    def __init__(self, serial_pin, clock_pin, latch_pin, timestep = 0.1, x=3, isWrapOn=False):
        
        #
        self.timestep = timestep
        self.x = x
        self.isWrapOn = isWrapOn
        
        # CRUCIAL FIX 1: Must be the private attribute __shifter (double underscore)
        self.__shifter = Shifter(serial_pin, clock_pin, latch_pin)

        self._is_running = False

        # FIX: Initialize the display to show starting position
        self.__shifter.shiftByte(1 << self.x)

    def move_step_display(self):

        # CRUCIAL FIX 2: Must be [-1, 1] to allow movement in both left and right directions
        step = random.choice([-1, 1]) 
        new_x = self.x + step

        if self.isWrapOn:
            #Wrapping around 0-7
            self.x = (new_x + 8) % 8
        else:
            # If the new positions is within 0-7 accept it
            if new_x >= 0 and new_x <= 7:
                self.x = new_x

        #Updating Display - converting the position
        data_to_send = 1 << self.x
        
        # CRUCIAL FIX 3: Must call shiftByte() here to update the LED display
        self.__shifter.shiftByte(data_to_send)

    def start(self):
        # FIX: Just set the running flag - don't use infinite loop here
        self._is_running = True
        # FIX: Make sure LED is on when starting
        self.__shifter.shiftByte(1 << self.x)

    def stop(self):
        #Just stops the movement the turns the led off
        self._is_running = False
        #Displays 0x00
        self.__shifter.shiftByte(0x00)

    # FIX: Added step method for controlled movement from main loop
    def step(self):
        """Execute one movement step if running - called from main loop"""
        if self._is_running:
            self.move_step_display()
            return True
        return False