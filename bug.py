<<<<<<< HEAD
##Kalp Upadhayay
#ENME441 - Lab 6 

#Bug.py program to run

import RPi.GPIO as GPIO
import time
from shifter import bug 

#Defining Pins

serial_pin = 23
clock_pin = 24
latch_pin = 25

#Pull up and Down Pins

s1_pin = 26 # On/Off 
s2_pin = 19 # Wrap control 
s3_pin = 13 # controls the speed

# --- 2. GLOBAL SETTINGS ---
GPIO.setmode(GPIO.BCM)
DEFAULT_TIMESTEP= 0.1 #setting the base speed

# Debounce time for switches to prevent multiple reads on a single press
DEBOUNCE_TIME = 0.2

bug = Bug(serial_pin, clock_pin, latch_pin)

#GPIO pins setup
GPIO.setup(s1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:

	while True:
		s1_state = GPIO.input(s1_PIN)
        s2_state = GPIO.input(s1_PIN)
        s3_state = GPIO.input(s3_PIN)


         # ------------On Off Control -------------------------------------------
        if s1_state == GPIO.HIGH:
            # S1 ON: Move the Bug one step
            bug.move_step_display()
            
            # Wait for the required time step 
            time.sleep(bug.timestep)
            
        else:
            # S1 OFF: Turn off the display
            bug.stop() 
            time.sleep(0.01) # Small pause when idle to reduce CPU load
        
        # -----------------Speed Control----------------------------------------
        if s3_state == GPIO.HIGH:
            # reducing dalay by factor of 3
            bug.timestep = DEFAULT_TIMESTEP / 3.0 
        else:
            bug.timestep = DEFAULT_TIMESTEP
        
        # ----------------Warp State Fixed----------------------------------
        # flip only when button is pressed high to low
        if prev_s2_state == GPIO.LOW and s2_state == GPIO.HIGH:
            bug.isWrapOn = not bug.isWrapOn
            # Simplified print statement: only shows the state change
            print(f"Wrap Mode Flipped: {'ON' if bug.isWrapOn else 'OFF'}") 
            # pause....
            time.sleep(DEBOUNCE_TIME) 
            
        prev_s2_state = s2_state # Update state for next loop iteration
        

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    
    finally:
        # Clean up GPIO settings on exit
        bug.stop() # Ensure the display is explicitly turned off
        GPIO.cleanup()
=======
##Kalp Upadhayay
#ENME441 - Lab 6 

#Bug.py program to run

import RPi.GPIO as GPIO
import time
from shifter import bug 

#Defining Pins

serial_pin = 23
clock_pin = 24
latch_pin = 25

#Pull up and Down Pins

s1_pin = 26 # On/Off 
s2_pin = 19 # Wrap control 
s3_pin = 13 # controls the speed

# --- 2. GLOBAL SETTINGS ---
GPIO.setmode(GPIO.BCM)
DEFAULT_TIMESTEP= 0.1 #setting the base speed

# Debounce time for switches to prevent multiple reads on a single press
DEBOUNCE_TIME = 0.2

bug = Bug(serial_pin, clock_pin, latch_pin)

#GPIO pins setup
GPIO.setup(s1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:

	while True:
		s1_state = GPIO.input(s1_PIN)
        s2_state = GPIO.input(s1_PIN)
        s3_state = GPIO.input(s3_PIN)


         # ------------On Off Control -------------------------------------------
        if s1_state == GPIO.HIGH:
            # S1 ON: Move the Bug one step
            bug.move_step_display()
            
            # Wait for the required time step 
            time.sleep(bug.timestep)
            
        else:
            # S1 OFF: Turn off the display
            bug.stop() 
            time.sleep(0.01) # Small pause when idle to reduce CPU load
        
        # -----------------Speed Control----------------------------------------
        if s3_state == GPIO.HIGH:
            # reducing dalay by factor of 3
            bug.timestep = DEFAULT_TIMESTEP / 3.0 
        else:
            bug.timestep = DEFAULT_TIMESTEP
        
        # ----------------Warp State Fixed----------------------------------
        # flip only when button is pressed high to low
        if prev_s2_state == GPIO.LOW and s2_state == GPIO.HIGH:
            bug.isWrapOn = not bug.isWrapOn
            # Simplified print statement: only shows the state change
            print(f"Wrap Mode Flipped: {'ON' if bug.isWrapOn else 'OFF'}") 
            # pause....
            time.sleep(DEBOUNCE_TIME) 
            
        prev_s2_state = s2_state # Update state for next loop iteration
        

    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    
    finally:
        # Clean up GPIO settings on exit
        bug.stop() # Ensure the display is explicitly turned off
        GPIO.cleanup()
>>>>>>> 9bfe8d8 (Created new test file)
