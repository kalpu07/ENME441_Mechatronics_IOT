#Kalp Upadhayay 
#ENME441 - Lab 6 Shift Registers

#Bug.py Program

import RPi.GPIO as GPIO
import time
import random
from Lab6_shifter import Bug  # Import Bug class

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

#Setup for Serial Clock Latch Pins
serial_pin = 23
clock_pin = 25
latch_pin = 24

# Switch pins
s1_pin = 26  # s1 = on off switch
s2_pin = 19  # s2 = wrap on or off switch 
s3_pin = 13  # s3 = speed increase switch

# Setup switch pins as inputs
GPIO.setup(s1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create Bug with pins above
bug = Bug(serial_pin, clock_pin, latch_pin)


#Variables trakc the current state of the object
prev_s2_state = GPIO.input(s2_pin) #S2's last state
last_move_time = 0                 #Just tracks when the bug last moved
default_speed = bug.timestep       # normal speed

try:
    print("Bug is working")
    
    while True:

        #Getting the current time
        current_time = time.time()
        
        # Monitering 3 GPIO switches
        s1_state = GPIO.input(s1_pin)
        s2_state = GPIO.input(s2_pin) 
        s3_state = GPIO.input(s3_pin)
        
        # Bug On or Off
        if s1_state == GPIO.HIGH:
            if bug.is_moving == False:
                bug.start()
        else:
            if bug.is_moving == True:
                bug.stop()
        
        # Flips the wrap when changed
        if s2_state != prev_s2_state:
            if s2_state == GPIO.HIGH: 
                bug.isWrapOn = not bug.isWrapOn

                if bug.isWrapOn:
                    print("Wrap mode is now ON")
                else:
                    print("Wrap mode is now OFF")

            prev_s2_state = s2_state
        
        # Changes the speed to 3 times when changed
        if s3_state == GPIO.HIGH:
            bug.timestep = default_speed / 3
        else:
            bug.timestep = default_speed
        
        # Move bug if it's running and time for next step
        if bug.is_moving:
            if current_time - last_move_time >= bug.timestep:
                bug.move()
                last_move_time = current_time
        
        time.sleep(0.01) #Adding small delay

except KeyboardInterrupt:
    print("\nProgram stopped")

finally:
    # Clean up
    bug.stop()
    GPIO.cleanup()