##Kalp Upadhayay
#ENME441 - Lab 6 

# Bug File

#Bug.py program to run

import RPi.GPIO as GPIO
import time
from Lab6_shifter import Bug 

#Defining Pins

serial_pin = 23
clock_pin = 24
latch_pin = 25

#Pull up and Down Pins

s1_pin = 26 # On/Off 
s2_pin = 19 # Wrap control 
s3_pin = 13 # controls the speed

