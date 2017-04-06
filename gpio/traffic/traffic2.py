#!/usr/bin/python
import time
import datetime
import RPi.GPIO as GPIO

def red():
    return 11

def yellow():
    return 7

def green():
    return 13

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
    p = GPIO.PWM(led(), 50)
    p.start(0)
    if nbFlash > 0:
        pulse(p, nbFlash)
    p.ChangeDutyCycle(100)
    time.sleep(nbSecAfterFlash)
    p.stop()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(red(), GPIO.OUT)
pRed =  GPIO.PWM(red(), 50)
pRed.start(0)

GPIO.setup(yellow(), GPIO.OUT)
pYellow =  GPIO.PWM(yellow(), 50)
pYellow.start(0)

GPIO.setup(green(), GPIO.OUT)
pGreen =  GPIO.PWM(green(), 50)
pGreen.start(0)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    nb = 0
    state = 0
    while True:
        input_state = GPIO.input(18)
        if input_state == False:
            state = (state + 1) % 6
            print("[{1}] {2} Button Pressed ! State: {0}".format(state,datetime.datetime.now(),nb))
            if state % 2 == 0:
                print("[{0}] {1} Its time to stop".format(datetime.datetime.now(),nb))
                pRed.ChangeDutyCycle(0)
                pYellow.ChangeDutyCycle(0)
                pGreen.ChangeDutyCycle(0)
            if state == 1:
                print("[{1}] {2} Its time for {0}".format("red",datetime.datetime.now(),nb))
                pRed.ChangeDutyCycle(100)
            if state == 3:
                pass
                print("[{1}] {2} Its time for {0}".format("green",datetime.datetime.now(),nb))
                pYellow.ChangeDutyCycle(100)
            if state == 5:
                print("[{1}] {2} Its time for {0}".format("yellow",datetime.datetime.now(),nb))
                pGreen.ChangeDutyCycle(100)
            # if(nb < 250):
            time.sleep(0.025)
            # else:
            #     time.sleep(0.5)
            nb = nb + 1
    #    nb = nb + 1
    #    print("[{1}] Cycle #{0}".format(nb,datetime.datetime.now()))
    #    Its(red, 1)
    #    time.sleep(0.5)
    #    Its(green, 1, 7)
    #    Its(yellow, 1)
    #    print("[{0}] End Of Cycle".format(datetime.datetime.now()))
    #    print("============================")
except KeyboardInterrupt:
    print("Interrupted by Keyboard")
    
pRed.start(0)
GPIO.output(red(), False)

pYellow.start(0)
GPIO.output(green(), False)

pGreen.start(0)
GPIO.output(yellow(), False)

GPIO.cleanup()
print("Time to stop")
