#!/usr/bin/python
import time
import datetime
import RPi.GPIO as GPIO

RED = 11
YELLOW = 7
GREEN = 13

class Led(object):
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        GPIO.setup(self.pin, GPIO.OUT)
        self.gpio = GPIO.PWM(self.pin, 50)
        self.gpio.start(0)

    def intensity(self, value):
        self.gpio.ChangeDutyCycle(value)

    def on(self):
        self.intensity(100)

    def off(self):
        self.intensity(0)
    
    def kill(self):
        self.gpio.stop()
        GPIO.output(self.pin, False)

def pulse(led, nb):
    print("    -> Will blink {0} times".format(nb))
    for k in range(nb):
        time.sleep(0.1)
        for i in range(100):
            led.intensity(i)
            time.sleep(0.001)
        time.sleep(0.25)
        for i in range(100):
            led.intensity(100 - (i))
            time.sleep(0.001)
        led.off()


def Its(led, nbSecAfterFlash, nbFlash=0):
    print("[{1}] Its time for {0}".format(led.name,datetime.datetime.now()))
    if nbFlash > 0:
        pulse(led, nbFlash)
    led.on()
    time.sleep(nbSecAfterFlash)
    led.off()


GPIO.setmode(GPIO.BOARD)

red = Led(RED,"red")
yellow = Led(YELLOW,"yellow")
green = Led(GREEN,"green")

try:
    nb = 0
    while True:
        nb = nb + 1
        print("[{1}] Cycle #{0}".format(nb,datetime.datetime.now()))
        Its(red, 12)
        time.sleep(0.5)
        Its(green, 6, 7)
        Its(yellow, 3)
        print("[{0}] End Of Cycle".format(datetime.datetime.now()))
        print("============================")
except KeyboardInterrupt:
    print("Interrupted by Keyboard")
    

red.kill()
yellow.kill()
green.kill()

GPIO.cleanup()
print("Time to stop")
