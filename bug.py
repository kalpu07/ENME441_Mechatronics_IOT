import RPi.GPIO as GPIO
import time
import random
from Lab6_shifter import Shifter  # Import your Shifter class

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# a. Instantiate a Shifter object
shifter = Shifter(23, 25, 24)  # serial, clock, latch pins

# Initialize variables
current_position = 3  # Start in the middle (position 3)
timestep = 0.05  # 0.05 second time step

try:
    
    while True:
        # b. Random walk: move by -1 or +1 with equal probability
        step = random.choice([-1, 1])
        new_position = current_position + step
        
        # Prevent moving beyond left or right edges (0-7)
        if 0 <= new_position <= 7:
            current_position = new_position
        
        # Display the current LED position
        # Convert position to bit pattern (1 << position lights just that LED)
        led_pattern = 1 << current_position
        shifter.shiftByte(led_pattern)
        
        # Wait for the time step
        time.sleep(timestep)

except KeyboardInterrupt:
    print("\nRandom walk stopped")

finally:
    # Clean up
    shifter.shiftByte(0)  # Turn off all LEDs
    GPIO.cleanup()