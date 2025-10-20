#Kalp Upadhayay 
#ENME441 - Lab 5: Pulse Width Modulation (PWM) and Threaded Callbacks

#Importing all neccessary libraries/modules
import math
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

#Creating a list of led pin numbers that loops from 2 to 11 ----- 10 led pins total
led_pins = list(range(2,12))

#Creating an empty list for pwms
pwms = []

f = 0.2 #frequency
base_frequency = 500 # Base frequency

button_pin = 17 # THis pin is my "button pin"

direction = 1 #Setting direction initially to 1

# Function to flip the direction of the LED by multiplying the direction by -1
def change_direction(channel): #Function will be automatically triggered when jumper wire connrected to 3.3
	global direction 
	direction *=-1

GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(button_pin, GPIO.RISING, callback = change_direction, bouncetime = 200)

phase_shift = (math.pi)/11

#Setting up each pin as a output and creating a different PWM instance for each
for pin in led_pins:
	GPIO.setup(pin, GPIO.OUT)
	pwm = GPIO.PWM(pin, base_frequency) # Starting with base frequency 500 hz
	pwm.start(0) # initiate PWM at 0% duty cycle
	pwms.append(pwm)


try:
	while 1:

		for i, pwm in enumerate(pwms):

			# Incrementing phase shift depending on current i value
			curr_phase = i * phase_shift * direction

			t= time.time() # getting current time
			curr_B = ((math.sin(2*math.pi*f*t - curr_phase))**2) # Brightness equation
			curr_dc = curr_B * 100 #converting to duty cycle percentage

			pwm.ChangeDutyCycle(curr_dc) #Updating current PWM

		#pwm.ChangeDutyCycle(B) # set duty cycle
		#pwm_2.ChangeDutyCycle(B) #Setting duty to 2


except KeyboardInterrupt: # stop gracefully on ctrl-C
	print('\nExiting')

# Stopping / Cleaning up each pin using for loop again
for pwm in pwms:
	pwm.stop()
	
GPIO.cleanup()







