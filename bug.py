#Kalp Upadhayay FINAL

import RPi.GPIO as GPIO
import time
import random
from Lab6_shifter import Bug  # Import Bug class

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Switch pins
s1_pin = 26  # On/Off switch
s2_pin = 19  # Wrap toggle switch  
s3_pin = 13  # Speed switch

# Setup switch pins as inputs
GPIO.setup(s1_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create Bug with default values
bug = Bug(23, 25, 24)

# Track states
prev_s2_state = GPIO.input(s2_pin)
last_move_time = 0
default_speed = bug.timestep

try:
    print("Bug Controller Ready!")
    print("S1: On/Off, S2: Wrap Toggle, S3: 3x Speed")
    
    while True:
        current_time = time.time()
        
        # a. Monitor 3 GPIO inputs
        s1_state = GPIO.input(s1_pin)
        s2_state = GPIO.input(s2_pin) 
        s3_state = GPIO.input(s3_pin)
        
        # b. S1 controls On/Off
        if s1_state == GPIO.HIGH:
            if not bug.is_moving:
                bug.start()
        else:
            if bug.is_moving:
                bug.stop()
        
        # c. S2 flips wrap state on change
        if s2_state != prev_s2_state:
            if s2_state == GPIO.HIGH:  # Only flip on button press
                bug.isWrapOn = not bug.isWrapOn
                print(f"Wrap: {'ON' if bug.isWrapOn else 'OFF'}")
            prev_s2_state = s2_state
        
        # d. S3 controls speed (3x when pressed)
        if s3_state == GPIO.HIGH:
            bug.timestep = default_speed / 3
        else:
            bug.timestep = default_speed
        
        # Move bug if it's running and time for next step
        if bug.is_moving and (current_time - last_move_time >= bug.timestep):
            bug.move()
            last_move_time = current_time
        
        time.sleep(0.01)  # Small delay to reduce CPU load

except KeyboardInterrupt:
    print("\nProgram stopped")

finally:
    # Clean up
    bug.stop()
    GPIO.cleanup()