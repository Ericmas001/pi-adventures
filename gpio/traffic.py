#!/usr/bin/python
import time
import RPi.GPIO as GPIO

RED = 11
YELLOW = 7
GREEN = 13


def pulse(p, nb):
    print("I blink {0} times".format(nb))
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
    print("I am {0}".format(led))
    p = GPIO.PWM(led, 50)
    p.start(0)
    pulse(p, nbFlash)
    p.ChangeDutyCycle(100)
    time.sleep(nbSecAfterFlash)
    p.stop()

GPIO.setmode(GPIO.BOARD)
bsdfgsdfgsdrgdstgtttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt = 0
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

try:
    while True:
        Its(RED, 2)
        time.sleep(0.5)
        Its(GREEN, 1, 7)
        Its(YELLOW, 0.5)
except KeyboardInterrupt:
    pass

GPIO.output(RED, False)
GPIO.output(GREEN, False)
GPIO.output(YELLOW, False)

GPIO.cleanup()
