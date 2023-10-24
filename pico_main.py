import network
import socket
import utime
from machine import Pin, PWM

ssid = "SkylarsHotspot"
password = "wifiPassword1"

motor1 = [
    Pin(15, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    ]

forward_seq = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1],
    ]
backward_seq = [
    [0,0,0,1],
    [0,0,1,0],
    [0,1,0,0],
    [1,0,0,0],
    ]

ticks_per_icnh = (513) / (2 * 3.14 * 2.3622)

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
    html_data = html_data.replace('{m1_state}', 'HELLO!')
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

##### Moving Functions #####

def forward(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)
    
#     # Motor 2. Not Real yet
#     for x in range(513 * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
#         for step in forward_seq:
#             for i in range(len(motor2)):
#                 motor1[i].value(step[i])
#                 utime.sleep(0.001)

def backward(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)
    
#     # Motor 2. Not Real yet
#     for x in range(513 * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
#         for step in backward_seq:
#             for i in range(len(motor2)):
#                 motor1[i].value(step[i])
#                 utime.sleep(0.001)

def left_middle_axis(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)
    
#     # Motor 2. Not Real yet
#     for x in range(513 * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
#         for step in backward_seq:
#             for i in range(len(motor2)):
#                 motor1[i].value(step[i])
#                 utime.sleep(0.001)

def right_middle_axis(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)
    
#     # Motor 2. Not Real yet
#     for x in range(513 * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
#         for step in forward_seq:
#             for i in range(len(motor2)):
#                 motor1[i].value(step[i])
#                 utime.sleep(0.001)

def custom_move(multiplier, speed, motor_1_rot, motor_2_rot):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in motor_1_rot:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001*speed)
    
#     # Motor 2. Not Real yet
#     for x in range(513 * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
#         for step in motor_2_rot:
#             for i in range(len(motor2)):
#                 motor1[i].value(step[i])
#                 utime.sleep(0.001*speed)

###################################

def draw1():
    forward(10)
    backward(5)
    
def draw2():
    forward(5)
    backward(5)
    forward(5)

def draw3():
    forward(2)
    backward(7)

try:
    pico_ip = connect()
    connection = open_socket(pico_ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()