from machine import Pin, PWM
import utime

motor1 = [
    Pin(15, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    ]

motor2 = [
    Pin(12, Pin.OUT),
    Pin(13, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT),
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

m1 = 'OFF'
m2 = "OFF"
s = "PEN UP"
tbot = "IDLE"
p = "NONE"
con_f = ""

ticks_per_icnh = (513) / (2 * 3.14 * 2.3622)

##### Pen Functions #####
def penup():
    pass

def pendown():
    pass

##### Moving Functions #####

def forward(multiplier):
    global con_f
    con_f = multiplier + "Forwards"
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:

            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[3-i])
                utime.sleep(0.001)
    con_f = ""

def backward(multiplier):
    global con_f
    con_f = multiplier + "Backwards"
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[3-i])
                utime.sleep(0.001)
    con_f = ""


def left_middle_axis(multiplier):
    global con_f
    con_f = multiplier + "Left"
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[i])
                utime.sleep(0.001)
    con_f = ""

def right_middle_axis(multiplier):
    global con_f
    con_f = multiplier + "Right"
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[i])
                utime.sleep(0.001)
    con_f = ""