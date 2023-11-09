from machine import Pin, PWM
import utime
from time import sleep

led = Pin(0, Pin.OUT)

motor1 = [
    Pin(14, Pin.OUT),
    Pin(15, Pin.OUT),
    Pin(16, Pin.OUT),
    Pin(17, Pin.OUT),
    ]

motor2 = [
    Pin(12, Pin.OUT),
    Pin(13, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(19, Pin.OUT),
    ]

servo = PWM(Pin(11))

S_DOWN = 1500000
S_UP = 1000000

servo.freq(50)
servo.duty_ns(S_UP)

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

cycle_speed = 0.001

m1 = 'OFF'
m2 = "OFF"
s = "PEN UP"
tbot = "IDLE"
p = "NONE"
con_f = ""

turning_slope = (53/1875)
wheel_r = 1.75
wheel_c = 2 * 3.14 * wheel_r
ticks_per_icnh = (513) / wheel_c

##### LED Functions #####
def led_waiting():
    for i in range(2):
        led.value(1)
        sleep(.2)
        led.value(0)
        sleep(.2)

def led_failed():
    for i in range(3):
        led.value(1)
        sleep(.05)
        led.value(0)
        sleep(.05)

def led_on():
    led.value(1)

##### Pen Functions #####
def penup():
    servo.duty_ns(S_UP)

def pendown():
    servo.duty_ns(S_DOWN)

##### Moving Functions #####

def forward(multiplier):
    global con_f
    con_f = str(multiplier) + " Forwards"

    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:

            for i in range(len(motor1)):
                motor1[i].value(step[i])
                sleep(cycle_speed)

                motor2[i].value(step[3-i])
                sleep(cycle_speed)
    con_f = ""

def backward(multiplier):
    global con_f
    con_f = str(multiplier) + " Backwards"
    # Motor 1
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(cycle_speed)

                motor2[i].value(step[3-i])
                utime.sleep(cycle_speed)
    con_f = ""


def left_middle_axis(turn_degrees):
    global con_f
    #con_f = str(multiplier) + " Left"
    
    multiplier = turning_slope * turn_degrees
    
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in forward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(cycle_speed)

                motor2[i].value(step[i])
                utime.sleep(cycle_speed)
    con_f = ""

def right_middle_axis(turn_degrees):
    global con_f
    #con_f = str(multiplier) + " Right"
    
    multiplier = turning_slope * turn_degrees
    
    for x in range(ticks_per_icnh * multiplier): # 6cm diameter wheel, circum. is 18.85 cm
        for step in backward_seq:
            for i in range(len(motor1)):
                motor1[i].value(step[i])
                utime.sleep(cycle_speed)

                motor2[i].value(step[i])
                utime.sleep(cycle_speed)
    con_f = ""

