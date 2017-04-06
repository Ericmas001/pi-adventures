#!/usr/bin/python
import time
import datetime
import RPi.GPIO as GPIO


RED = 11
YELLOW = 7
GREEN = 13

def red():
    return pRed

def yellow():
    return pYellow

def green():
    return pGreen

def pulse(p, nb):
    print("    -> Will blink {0} times".format(nb))
    for k in range(nb):
        time.sleep(0.1)
        for i in range(100):
            p.ChangeDutyCycle(i)
            time.sleep(0.001)
        time.sleep(0.25)
        for i in range(100):
            p.ChangeDutyCycle(100 - (i))
            time.sleep(0.001)
        p.ChangeDutyCycle(0)


def Its(led, nbSecAfterFlash, nbFlash=0):
    print("[{1}] Its time for {0}".format(led.__name__,datetime.datetime.now()))
    if nbFlash > 0:
        pulse(led(), nbFlash)
    led().ChangeDutyCycle(100)
    time.sleep(nbSecAfterFlash)
    led().ChangeDutyCycle(0)


GPIO.setmode(GPIO.BOARD)

GPIO.setup(RED, GPIO.OUT)
pRed = GPIO.PWM(RED, 50)
pRed.start(0)

GPIO.setup(YELLOW, GPIO.OUT)
pYellow = GPIO.PWM(YELLOW, 50)
pYellow.start(0)

GPIO.setup(GREEN, GPIO.OUT)
pGreen = GPIO.PWM(GREEN, 50)
pGreen.start(0)

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
    

pRed.stop()
GPIO.output(RED, False)

pYellow.stop()
GPIO.output(YELLOW, False)

pGreen.stop()
GPIO.output(GREEN, False)

GPIO.cleanup()
print("Time to stop")
