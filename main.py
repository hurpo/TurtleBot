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
    html = f"""
<!DOCTYPE html>
<head>
    <title>Turtle Bot Control Hub</title>
    <style type="text/css">
        body {
            background-color: blue;
        }

        h1 {
            color: #54ff93;
            font-family: 'Courier New', Courier, monospace;
        }

        p {
            color: white;
        }

        input {
            font-size: large;
            background-color: black;
        }
    </style>
</head>
<body>
    <h1>Turtle Bot</h1>
    <form action="./draw1">
        <input type="submit" value="Draw1"/>
    </form>
    <form action="./draw2">
        <input type="submit" value="Draw2"/>
    </form>
    <form action="./draw3">
        <input type="submit" value="Draw3"/>
    </form>
</body>"""
    return str(html)

def style():
    css = f"""
body {
    color: black;
}

h1, h2, h3 {
    margin: 0%;
}

h1 {
    font-size:370%;
}

header {
    margin-left: 5%;
    margin-right: 5%;
    margin-top: 5%;
    margin-bottom: .6%;
}

input {
    font-size: large;
    background-color: cadetblue;
}
"""
    return str(css)

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
        client.send(html)
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