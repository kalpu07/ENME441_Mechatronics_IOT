# webserver.py
#
# Web server via sockets.
#
# When contacted by a client (web browser), send a web page
# displaying the states of selected GPIO pins.
#
# Must run as sudo to access port 80.  
#
# Port 8080 is a non-privileged alternative to port 80 that can
# be used to avoid the need for sudo, if desired.

import socket
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pins = [17,22,27]
brightnesses = [0, 0, 0]
led_pwm = []

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 1000)  # 1000 Hz frequency
    pwm.start(0)  # Start with 0% duty cycle
    led_pwm.append(pwm)

#Code got fromm Professors prasePOSdata
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

# Generate HTML for the web page:
def web_page():
    rows = [f'<tr><td>{p}</td><td>{GPIO.input(p)}</td></tr>' for p in pins]
    html = f"""
    <html>
        <head> 
            <title>LED LEVELS</title> 
        </head>
        <body> 
            <h1>Select LED</h1>
            <form method="POST">
                <h3> Brightness Level: </h3>
                <input type="range" name="brightness" min ="0" max="100" value ="500"/>
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
        # Use our simple function to read the form data
            form_data = parsePOSTdata(request.decode('utf-8'))
    
            # Now you can get the values
            if 'led' in form_data and 'brightness' in form_data:
                led_number = int(form_data['led'])  # Convert string to number
                brightness = int(form_data['brightness'])  # Convert string to number

                led_index = led_number - 1  # Convert to 0-based index (LED1=0, LED2=1, LED3=2)
                led_pwm[led_index].ChangeDutyCycle(brightness)
                brightnesses[led_index] = brightness  # Also update your brightness tracking array
            
                # Update your LED here
                print(f"Setting LED {led_number} to {brightness}%")

        conn.send(b'HTTP/1.1 200 OK\r\n')         # status line 
        conn.send(b'Content-type: text/html\r\n') # header (content type)
        conn.send(b'Connection: close\r\n\r\n')   # header (tell client to close)
        # send body in try block in case connection is interrupted:
        try:
            conn.sendall(web_page())                    # body
        finally:
            conn.close()

serve_web_page()