# Kalp Upadhayay 
# ENME441 - Fall - 2025
#
# Lab 7 Question 1 Code
# 
# Note: webserver.py code from Repo used and built on top of 
# Can select an LED and adjust its bridhgness through Web interface

import socket
import RPi.GPIO as GPIO
import time

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

#Setting Pin Values
pin_1 = 18
pin_2 = 23
pin_3 = 24

#Used for tracking all LEDs
brightnesses = [0, 0, 0]

#Stores the PWM objects 
led_pwm = []

#Setting Up PWM for each of three LEDS

#I used for Debugging Purposes -------------------------------
try:
    #Setting up all GPIO Pins
    GPIO.setup(pin_1, GPIO.OUT)
    GPIO.setup(pin_2, GPIO.OUT)
    GPIO.setup(pin_3, GPIO.OUT)

    #Instances being created for all three PWMs leds
    pwm_1 = GPIO.PWM(pin_1, 100)
    pwm_2 = GPIO.PWM(pin_2, 100)
    pwm_3 = GPIO.PWM(pin_3, 100)

    #Starting with 0 duty cycles
    pwm_1.start(0)
    pwm_2.start(0)
    pwm_3.start(0)

    #Storing within List 
    led_pwm.append(pwm_1)
    led_pwm.append(pwm_2)
    led_pwm.append(pwm_3)

    print("GPIO SETUP IS WORKING")

except Exception as e:
    print(f"GPIO PIN Setup NOT WORKING: {e}")
    exit(1)

#Parse Helper Function @web_gpio_POST.py
def parsePOSTdata(data):
    data_dict = {}
    idx = data.find('\r\n\r\n')+4
    data = data[idx:]
    data_pairs = data.split('&')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict

# Generate HTML for the web page: Referenced webserver.py sample code
#Creating a simple HTML with radio buttons and a slider
def web_page():
    html = f"""
    <html>
        <head> 
            <title>LED LEVELS</title> 
        </head>
        <body> 
            <h1>Select LED</h1>
            <form action="/" method="POST">
                <h3> Brightness Level: </h3>
                <input type="range" name="brightness" min ="0" max="100" value ="100"/>
                <h3> Select LED: </h3>
                <p> <input type="radio" name="led" value="1"> LED1: {brightnesses[0]}% </p>
                <p> <input type="radio" name="led" value="2"> LED2: {brightnesses[1]}% </p>
                <p> <input type="radio" name="led" value="3"> LED3: {brightnesses[2]}% </p>
                <input type="submit" name="submit" value="Change Brightness">
            </form>
        </body>
    </html>
        """
    print(html)
    return (bytes(html,'utf-8'))   # convert string to UTF-8 bytes object
     
# Serve the web page to a client on connection:
def serve_web_page():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP-IP socket
    s.bind(('', 80))
    s.listen(1)  # up to 3 queued connections
    while True:
        time.sleep(0.1)
        print('Waiting for connection...')
        conn, (client_ip, client_port) = s.accept()     # blocking call
        request = conn.recv(1024)                 # read request (required even if none)
        print(f'Connection from {client_ip}')   

        if request.startswith(b'POST'):
        # Reading Form Data through Parse
            form_data = parsePOSTdata(request.decode('utf-8'))
    
            # Now you can get the values
            if 'led' in form_data and 'brightness' in form_data:
                led_number = int(form_data['led'])  #Both strings get converted to numbers
                brightness = int(form_data['brightness'])  

                led_index = led_number - 1  # Have to subtract 1 due to indexing
                led_pwm[led_index].ChangeDutyCycle(brightness)
                brightnesses[led_index] = brightness  # Updating brightness 
            
                # Update your LED here
                print(f"Setting LED {led_number} to {brightness}%")

        conn.send(b'HTTP/1.1 200 OK\r\n')         # status line 
        conn.send(b'Content-type: text/html\r\n') # header (content type)
        conn.send(b'Connection: close\r\n\r\n')   # header (tell client to close)
        # send body in try block in case connection is interrupted:
        try:
            conn.sendall(web_page())                    
        finally:
            conn.close()

serve_web_page()