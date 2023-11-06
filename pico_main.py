import network
import socket
import utime
from machine import Pin, PWM
from pico_functions import *

ssid = "SkylarsHotspot"
password = "wifiPassword1"

##### Turtle Bot Online Control Hub Functions #####

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        utime.sleep(1)
    pico_ip = wlan.ifconfig()[0]
    print("Successful connection with " + str(pico_ip))
    return pico_ip

def open_socket(pico_ip):
    address = (pico_ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    html = open("./index.html", "r")
    html_data = html.read()
    html_data = html_data.replace('{m1_state}', m1)
    html_data = html_data.replace('{m2_state}', m2)
    html_data = html_data.replace('{s_state}', s)
    html_data = html_data.replace('{tbot_state}', tbot)
    html_data = html_data.replace('{p_state}', p)
    html_data = html_data.replace('{Console_Feed}', con_f)
    return html_data

def style():
    css = open("style.css", "r")
    return css.read() 

def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/draw1?':
            draw1()
        elif request == '/draw2?':
            draw2()
        elif request == '/draw3?':
            draw3()
        print(request)
        html = webpage()
        #css = style()
        client.send(html)
        #client.send(css)
        client.close()

def draw1():
    global tbot, p
    tbot = "RUNNING"
    p = "Draw 1"
    forward(10)
    backward(5)
    tbot = "IDLE"
    p = "NONE"
    
def draw2():
    global tbot, p
    tbot = "RUNNING"
    p = "Draw 2"
    forward(5)
    backward(5)
    forward(5)
    tbot = "IDLE"
    p = "NONE"

def draw3():
    global tbot, p
    tbot = "RUNNING"
    p = "Draw 3"
    forward(2)
    backward(7)
    tbot = "IDLE"
    p = "NONE"

def ieee_logo(a):
    global tbot, p
    tbot = "RUNNING"
    p = "IEEE Logo"
    # I
    forward(a)
    right_middle_axis(90)
    forward(a)
    left_middle_axis(90)
    forward(3*a)
    left_middle_axis(90)
    forward(a)
    right_middle_axis(90)
    forward(a)
    right_middle_axis(90)
    forward(2.5*a)
    right_middle_axis(90)
    forward(a)
    right_middle_axis(90)
    forward(a)
    left_middle_axis(90)
    forward(3*a)
    left_middle_axis(90)
    forward(a)
    right_middle_axis(90)
    forward(a)
    right_middle_axis(90)
    forward(2.5*a)
    penup()
    right_middle_axis(180)

    # 3 E's
    for i in range(3):
        forward(2*a)
        pendown()
        forward(1.5 * a)
        left_middle_axis(90)
        forward(a)
        left_middle_axis(90)
        forward(a)
        right_middle_axis(90)
        forward(a)
        right_middle_axis(90)
        forward(a)
        left_middle_axis(90)
        forward(a)
        left_middle_axis(90)
        forward(a)
        right_middle_axis(90)
        forward(a)
        right_middle_axis(90)
        forward(a)
        right_middle_axis(90)
        forward(a)
        left_middle_axis(90)
        forward(a)
        left_middle_axis(90)
        forward(1.5 * a)
        left_middle_axis(90)
        forward(5 * a)
        penup()
        left_middle_axis(90)
    tbot = "IDLE"
    p = "NONE"
    

try:
    pico_ip = connect()
    connection = open_socket(pico_ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
