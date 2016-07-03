#!/usr/bin/python

import subprocess
from datetime import datetime
import sys
from picamera import PiCamera
from time import sleep

class Console:
    @staticmethod
    def Write(str, *args):
        sys.stdout.write(str.format(*args))
        sys.stdout.flush()

    @staticmethod
    def WriteLine(str, *args):
        print str.format(*args)
        
def take_picture(camera, nb_ss, filename):
    Console.Write("Taking setting {0} ... ", nb_ss) 
    camera.framerate = float((float(101) - (float(nb_ss) / float(10))) / float(100))
    camera.shutter_speed = 10000 * nb_ss
    Console.Write("ss={0}, awb={1} ... ",camera.shutter_speed,camera.awb_gains)
    camera.capture("/Pictures/Flowers/{0}_{1:04d}.jpg".format(filename, nb_ss))
    Console.WriteLine("ok")
    
filename = datetime.today().strftime("%Y-%m-%d_%H.%M.%S")

Console.WriteLine("Taking pictures {0} !!!", filename)
camera = PiCamera(resolution=(2592, 1944))
try:
   
    camera.iso = 100
    sleep(2)
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    
    take_picture(camera, 5,filename)
    take_picture(camera, 10,filename)
    take_picture(camera, 50,filename)
    take_picture(camera, 100,filename)
    take_picture(camera, 200,filename)
    take_picture(camera, 300,filename)
    take_picture(camera, 500,filename)
    take_picture(camera, 1000,filename)
    
    pass
finally:
    camera.close()
