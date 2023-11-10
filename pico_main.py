import network
import socket
import json
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
    time_limit = 10
    while (wlan.isconnected() == False) and time_limit > 0:
        print("Waiting for connection...")
        utime.sleep(1)
        led_waiting()
        time_limit -= 1
    if time_limit == 0:
        print("Took too long, trying again.")
        led_failed()
        return connect()
    else:
        pico_ip = wlan.ifconfig()[0]
        print("Successful connection with " + str(pico_ip))
        led_on()
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
        print(request)
        if request == '/pen_down?':
            pendown_test()
        elif request == '/pen_up?':
            penup_test()
        elif request == '/square?':
            square()
        elif request == '/ieee_logo?':
            ieee_logo(0.5)
        if request == '/data':
            response = {'m1': m1,'m2': m2, "s": s, "tbot": tbot, "p": p}
            client.send(json.dumps(response))
        else:
        #css = style()
            html = webpage()
            client.send(html)
        #client.send(css)
        client.close()

def pendown_test():
    pendown()
    
def penup_test():
    penup()

def square():
    pendown()
    for i in range(4):
        forward(3)
        left_middle_axis(90)

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
        if (i > 0):
            forward(2*a)
        else:
            forward(3*a)
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
