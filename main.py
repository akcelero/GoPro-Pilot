import network
import socket
import json
import sys
from machine import Pin
from time import sleep

network.WLAN(network.AP_IF).active(False)
network.WLAN(network.STA_IF).active(False)

try:
    with open('credentials.config') as f:
        credentials = [line.replace('\n', '') for line in f.readlines()]
except:
    print('Can not open file with credentials')
    raise

if len(credentials) != 2:
    print('Wrong struct of credentials file, check example')
    raise Error()

essid = credentials[0]
password = credentials[1]

goproIP = '10.5.5.9'

shutterPath = '/gp/gpControl/command/shutter?p=1'
stopPath = '/gp/gpControl/command/shutter?p=0'
photoMode = '/gp/gpControl/command/mode?p=1'
videoMode = '/gp/gpControl/command/mode?p=0'
locateOn = '/gp/gpControl/command/system/locate?p=1'
locateOff = '/gp/gpControl/command/system/locate?p=0'
statusPath = '/gp/gpControl/status'

blue_led = Pin(12, Pin.OUT)
red_led = Pin(4, Pin.OUT)

button1 = Pin(13, Pin.IN)
button2 = Pin(14, Pin.IN)
button3 = Pin(16, Pin.IN)

blue_led.value(0)
red_led.value(0)


def action(path):
    soc = socket.socket()
    soc.connect((goproIP, 80))
    soc.send(
            b'GET ' + path + ' HTTP/1.0\r\nHost: ' + path + '\r\n\r\n'
    )
    data = soc.read()
    soc.close()
    return data


def toggle(pin):
    pin.value(not pin.value())


def turnOn(led):
    led.value(1)


def turnOff(led):
    led.value(0)


def button1Callback(trigger):
    turnOn(blue_led)
    action(photoMode)
    action(shutterPath)
    sleep(0.2)
    turnOff(blue_led)


def button2Callback(trigger):
    turnOn(blue_led)
    data = action(statusPath)
    capturing = json.loads(
        '{' + data.decode('utf-8').split('{', 1)[1].replace('\n', '')
    )['status']['8']
    if not capturing:
        action(videoMode)
    path = '/gp/gpControl/command/shutter?p=' + str(capturing ^ 1)
    action(path)
    turnOff(blue_led)


def button3Callback(trigger):
    turnOn(blue_led)
    data = action(statusPath)
    locate = json.loads(
        '{' + data.decode('utf-8').split('{', 1)[1].replace('\n', '')
    )['status']['45']
    path = '/gp/gpControl/command/system/locate?p=' + str(locate ^ 1)
    action(path)
    turnOff(blue_led)


# ------- Initialize connect with camera -----------

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(essid, password)

# ---- Inform about trying connect with camera -----

while not sta.isconnected():
    toggle(red_led)
    sleep(0.5)
turnOff(red_led)

# ------- Inform about succesful connection ---------

for i in range(8):
    toggle(blue_led)
    sleep(0.2)

# -------- Setup interrupts on buttons pins ----------

button1.irq(trigger=Pin.IRQ_FALLING, handler=button1Callback)
button2.irq(trigger=Pin.IRQ_FALLING, handler=button2Callback)
# GPIO16 has no IRQ function
# button3.irq(trigger=Pin.IRQ_FALLING, handler=button2Callback)

# Simulate callback at falling edge at button nr 3
prevStatusButton3 = button3.value()
while True:
    if prevStatusButton3 == 0 and not (prevStatusButton3 == button3.value()):
        button3Callback(button3)
    prevStatusButton3 = button3.value()
    sleep(0.2)
