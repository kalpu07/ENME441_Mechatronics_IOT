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

pins = (19,21,22,23,25,26,32,33)
for p in pins: GPIO.setup(p, GPIO.IN) 

# Generate HTML for the web page:
def web_page():
    rows = [f'<tr><td>{p}</td><td>{GPIO.input(p)}</td></tr>' for p in pins]
    html = """
    <html>
        <head> 
            <title>LED LEVELS</title> 
        </head>
        <body> 
            <h1>Select LED</h1>
            <form action="/cgi-bin/range.py" method="POST">
                <h3> Brightness Level: </h3>
                <input type="range" name="led brightness" min ="0" max="1000" value ="500"/>
                <h3> Select LED: </h3>
                <input type="radio" name="led type" value="LED1"> LED1
                <br/>
                <input type="radio" name="led type" value="LED2"> LED2
                <br/>
                <input type="radio" name="led type" value="LED3"> LED3
                <br/>
                <input type="submit" name="submit" value="Change Brightness"> Change Brightness
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
        conn.send(b'HTTP/1.1 200 OK\r\n')         # status line 
        conn.send(b'Content-type: text/html\r\n') # header (content type)
        conn.send(b'Connection: close\r\n\r\n')   # header (tell client to close)
        # send body in try block in case connection is interrupted:
        try:
            conn.sendall(web_page())                    # body
        finally:
            conn.close()

serve_web_page()