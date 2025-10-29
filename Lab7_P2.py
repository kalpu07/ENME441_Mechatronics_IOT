# Kalp Upadhayay 
# ENME441 - Fall - 2025
#
# Lab 7 Question 2 Code
# 
# Note: webserver.py code used and built on top of 

import socket
import RPi.GPIO as GPIO
import time

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)

#Setting Pin Values
pin_1 = 18
pin_2 = 23
pin_3 = 24

brightnesses = [0, 0, 0]
led_pwm = []

#Setting Up PWM for each of three LEDS

try:
    GPIO.setup(pin_1, GPIO.OUT)
    GPIO.setup(pin_2, GPIO.OUT)
    GPIO.setup(pin_3, GPIO.OUT)

    pwm_1 = GPIO.PWM(pin_1, 100)
    pwm_2 = GPIO.PWM(pin_2, 100)
    pwm_3 = GPIO.PWM(pin_3, 100)

    pwm_1.start(0)
    pwm_2.start(0)
    pwm_3.start(0)

    led_pwm.append(pwm_1)
    led_pwm.append(pwm_2)
    led_pwm.append(pwm_3)

    print("GPIO SETUP IS WORKING")

except Exception as e:
    print(f"GPIO PIN Setup ISSUE!!!!: {e}")
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
# Generate HTML for the web page with Javascript for automatic updates
def web_page():
    html = f"""
    <html>
        <head> 
            <title>LED Brightness Control</title> 
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .slider-container {{ margin: 25px 0; }}
                .slider-label {{ font-weight: bold; margin-bottom: 5px; }}
                .value-display {{ margin-left: 15px; font-weight: bold; }}
                input[type="range"] {{ width: 300px; }}
            </style>
            <script>
                function updateLED(ledNumber, brightness) {{
                    // Create XMLHttpRequest to send POST without page reload
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/", true);
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    
                    // Send the LED number and brightness value
                    var data = "led=" + ledNumber + "&brightness=" + brightness;
                    xhr.send(data);
                    
                    // Update the display for this LED
                    document.getElementById("value" + ledNumber).innerText = brightness + "%";
                    
                    console.log("LED " + ledNumber + " set to " + brightness + "%");
                }}
            </script>
        </head>
        <body> 
            <h1>LED Brightness Control</h1>
            <p><em>Move any slider to instantly update brightness - no submit button needed!</em></p>
            
            <div class="slider-container">
                <div class="slider-label">LED1</div>
                <input type="range" min="0" max="100" value="{brightnesses[0]}" 
                       oninput="updateLED(1, this.value)"
                       onchange="updateLED(1, this.value)">
                <span class="value-display" id="value1">{brightnesses[0]}%</span>
            </div>
            
            <div class="slider-container">
                <div class="slider-label">LED2</div>
                <input type="range" min="0" max="100" value="{brightnesses[1]}" 
                       oninput="updateLED(2, this.value)"
                       onchange="updateLED(2, this.value)">
                <span class="value-display" id="value2">{brightnesses[1]}%</span>
            </div>
            
            <div class="slider-container">
                <div class="slider-label">LED3</div>
                <input type="range" min="0" max="100" value="{brightnesses[2]}" 
                       oninput="updateLED(3, this.value)"
                       onchange="updateLED(3, this.value)">
                <span class="value-display" id="value3">{brightnesses[2]}%</span>
            </div>
            
            <div style="margin-top: 30px; color: #666;">
                <p>Changes are applied instantly without page reload.</p>
            </div>
        </body>
    </html>
    """
    return bytes(html, 'utf-8')
     
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