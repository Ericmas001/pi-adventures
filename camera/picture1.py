#!/usr/bin/python

import subprocess
from datetime import datetime
import sys
from picamera import PiCamera
from time import sleep
import io
import Image
import ImageStat
import math

class Console:
    @staticmethod
    def Write(str, *args):
        sys.stdout.write(str.format(*args))
        sys.stdout.flush()

    @staticmethod
    def WriteLine(str, *args):
        print str.format(*args)
    
def brightness( im_file ):
   im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]
    
def take_picture_stream(camera, nb_ss, filename):
    Console.Write("Taking stream, setting #{0} ... ", nb_ss) 
    my_stream = io.BytesIO()
    camera.framerate = float((float(101) - (float(nb_ss) / float(10))) / float(100))
    camera.shutter_speed = 10000 * nb_ss
    Console.Write("ss={0}, awb={1} ... ",camera.shutter_speed,camera.awb_gains)
    camera.capture(my_stream, 'jpeg')
    my_stream.seek(0)
    return my_stream
    
def take_best_picture(camera, filename):
    Console.WriteLine("Taking the best possible picture !!!") 
    min = 60
    max = 80
    ss = 1;
    bright = 0.1;
    bestbright = 0;
    beststream = io.BytesIO()
    count = 0;
    while(ss > 0 and ss < 1000 and count < 15 and (bright < min or bright > max) ):
        count+=1
        try:
            my_stream = take_picture_stream(camera, int(ss), filename)
            bright = brightness(my_stream)
            Console.WriteLine(" brighness={0} ... ok", bright)
            short = 0
            if (bestbright < min):
                short = min - bestbright
            if (bestbright > max):
                short = bestbright - max
            if(bright < min):
                if(min - bright < short):
                    bestbright = bright
                    beststream = my_stream
                ss *= 3
                if(bright < 10):
                    ss *= 10
                if(ss > 1000):
                    ss = 1000
                    ount = 14
            if(bright > max):
                if(bright - max < short):
                    bestbright = bright
                    beststream = my_stream
                ss *= 0.5
                if(bright > 300):
                    ss /= 10
                if(ss < 1):
                    ss = 0
            if(bright >= min and bright <= max):
                bestbright = bright
                beststream = my_stream
        except Exception as inst:
            Console.WriteLine("")
            print("Unexpected error:", sys.exc_info()[0])    
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst) 
            break;
    beststream.seek(0)
    Console.Write("Accepted brighness={0} ... let's write ... ", bestbright)
    open("/Pictures/Flowers/{0}_{1:04d}.jpg".format(filename, int(ss)), 'wb').write(beststream.read())
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
    
    take_best_picture(camera, filename)
    
    pass
finally:
    camera.close()
