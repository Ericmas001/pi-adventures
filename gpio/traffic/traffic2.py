#!/usr/bin/python
import time
import datetime
import RPi.GPIO as GPIO

RED = 11
YELLOW = 7
GREEN = 13
BUTTON = 18

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

GPIO.setmode(GPIO.BOARD)

red = Led(RED,"red")
yellow = Led(YELLOW,"yellow")
green = Led(GREEN,"green")
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    nb = 0
    state = 1
    leds = [red,yellow,green]
    while True:
        input_state = GPIO.input(BUTTON)
        if input_state == False:
            state = (state + 1) % 6
            print("[{1}] {2} Button Pressed ! State: {0} Button: {3} Becoming {4}".format(state,datetime.datetime.now(),nb, leds[int(state/2)].name, "on" if (state % 2) == 0 else "off"))
            leds[int(state/2)].intensity(((state+1) % 2)*100)
            time.sleep(0.25)
            nb = nb + 1
except KeyboardInterrupt:
    print("Interrupted by Keyboard")
    

red.kill()
yellow.kill()
green.kill()

GPIO.cleanup()
print("Time to stop")
