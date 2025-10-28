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
# Generate HTML for the web page with Javascript:
def web_page():
    html = f"""
    <html>
        <head> 
            <title>LED Control</title> 
            <script>
                function updateLED(ledNumber, brightness) {{
                    // Send POST request without reloading page
                    var xhr = new XMLHttpRequest();
                    xhr.open("POST", "/", true);
                    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                    
                    // Send which LED and what brightness
                    var data = "led=" + ledNumber + "&brightness=" + brightness;
                    xhr.send(data);
                    
                    // Update the display for this LED
                    document.getElementById("value" + ledNumber).innerText = brightness + "%";
                }}
            </script>
        </head>
        <body> 
            <h1>LED Brightness Control</h1>
            <p><strong>Move any slider to instantly update brightness</strong></p>
            
            <div style="margin: 20px 0;">
                <div style="margin: 15px 0;">
                    <strong>LED1</strong><br>
                    <input type="range" min="0" max="100" value="{brightnesses[0]}" 
                           oninput="updateLED(1, this.value)">
                    <span id="value1">{brightnesses[0]}%</span>
                </div>
                
                <div style="margin: 15px 0;">
                    <strong>LED2</strong><br>
                    <input type="range" min="0" max="100" value="{brightnesses[1]}" 
                           oninput="updateLED(2, this.value)">
                    <span id="value2">{brightnesses[1]}%</span>
                </div>
                
                <div style="margin: 15px 0;">
                    <strong>LED3</strong><br>
                    <input type="range" min="0" max="100" value="{brightnesses[2]}" 
                           oninput="updateLED(3, this.value)">
                    <span id="value3">{brightnesses[2]}%</span>
                </div>
            </div>
            
            <p><em>Changes are applied instantly without page reload</em></p>
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