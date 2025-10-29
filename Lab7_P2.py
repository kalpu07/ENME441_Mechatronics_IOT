# Kalp Upadhayay 
# ENME441 - Fall - 2025
#
# Lab 7 Question 2 Code
# 
# Note: webserver.py code used and built on top of 
# Can select an LED and adjust its bridhgness through Web interface, but this time automatic slider updates 
#Python remained the same webpage function used LLM 

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
# LLM Used Deepseek for HTML, SLider, CSS and Javascript
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
                let timeoutId = null;
                
                function updateLED(ledNumber, brightness) {{
                    // Update display immediately for responsiveness
                    document.getElementById("value" + ledNumber).innerText = brightness + "%";
                    
                    // Clear any pending request
                    if (timeoutId) clearTimeout(timeoutId);
                    
                    // Send request after a short delay (debounce)
                    timeoutId = setTimeout(function() {{
                        var xhr = new XMLHttpRequest();
                        xhr.open("POST", "/", true);
                        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                        var data = "led=" + ledNumber + "&brightness=" + brightness;
                        xhr.send(data);
                        console.log("LED " + ledNumber + " set to " + brightness + "%");
                    }}, 100); // 100ms delay
                }}
            </script>
        </head>
        <body> 
            <h1>LED Brightness Control</h1>
            <p><em>Move any slider to instantly update brightness</em></p>
            
            <div class="slider-container">
                <div class="slider-label">LED1</div>
                <input type="range" min="0" max="100" value="{brightnesses[0]}" 
                       oninput="updateLED(1, this.value)">
                <span class="value-display" id="value1">{brightnesses[0]}%</span>
            </div>
            
            <div class="slider-container">
                <div class="slider-label">LED2</div>
                <input type="range" min="0" max="100" value="{brightnesses[1]}" 
                       oninput="updateLED(2, this.value)">
                <span class="value-display" id="value2">{brightnesses[1]}%</span>
            </div>
            
            <div class="slider-container">
                <div class="slider-label">LED3</div>
                <input type="range" min="0" max="100" value="{brightnesses[2]}" 
                       oninput="updateLED(3, this.value)">
                <span class="value-display" id="value3">{brightnesses[2]}%</span>
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