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

ticks_per_icnh = (513) / (2 * 3.14 * 2.3622)

##### Pen Functions #####
def penup():
    pass

def pendown():
    pass

##### Moving Functions #####

def forward(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:

            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[3-i])
                utime.sleep(0.001)

def backward(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[3-i])
                utime.sleep(0.001)


def left_middle_axis(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[i])
                utime.sleep(0.001)

def right_middle_axis(multiplier):
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(0.001)

                motor2[i].value(step[i])
                utime.sleep(0.001)