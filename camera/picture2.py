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

def take_simple_picture(camera, filename):
    Console.Write("Taking simple picture ... ") 
    camera.capture("/Pictures/tests/{0}_a_simple.jpg".format(filename))
    Console.WriteLine("ok")
	
def take_corrected_picture(camera, filename):
    Console.Write("Taking corrected picture ... ") 
    camera.iso = 100
    sleep(2)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    Console.Write("ss={0}, awb={1} ... ",camera.shutter_speed,camera.awb_gains)
    camera.capture("/Pictures/tests/{0}_b_corrected.jpg".format(filename))
    Console.WriteLine("ok")
	
def take_5_corrected_pictures(camera, filename):
    Console.WriteLine("Taking 5 corrected picture ... ") 
    camera.iso = 100
    sleep(2)
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    for i in range(1,6):
        camera.shutter_speed = camera.shutter_speed * i
        Console.Write("ss={0}, awb={1} ... ",camera.shutter_speed,camera.awb_gains)
        camera.capture("/Pictures/tests/{0}_c_corrected_{1}.jpg".format(filename, i))
        Console.WriteLine("ok")
        
def take_picture(camera, nb_ss, filename):
    Console.Write("Taking setting {0} ... ", nb_ss) 
    camera.framerate = float((float(101) - (float(nb_ss) / float(10))) / float(100))
    camera.shutter_speed = 10000 * nb_ss
    Console.Write("ss={0}, awb={1} ... ",camera.shutter_speed,camera.awb_gains)
    camera.capture("/Pictures/tests/{0}_d_{1:04d}.jpg".format(filename, nb_ss))
    Console.WriteLine("ok")
""" 
def take_picture( camera, nb_ss, filename ):
   startprint( "Taking setting {0} ... ".format(nb_ss))
   camera.resolution = (2592, 1944)
   camera.iso = 100
   sleep(2)
   camera.shutter_speed = camera.exposure_speed
   camera.exposure_mode = 'off'
   g = camera.awb_gains
   camera.awb_mode = 'off'
   camera.awb_gains = g
   sleep(10)
#   camera.capture_sequence(['image%02d.jpg' % i for i in range(10)])
   camera.capture_sequence(["/Pictures/tests/{1}_{0:03d}.jpg".format(i, filename) for i in range(10)])

#   nopreview = "-n" # -n, --nopreview : Do not display a preview window
#   shutter = "-ss {0}00000".format(nb_ss) # -ss, --shutter  : Set shutter speed in microseconds
#   quality = "-q 100" # -q, --quality   : Set jpeg quality <0 to 100>
#   output = "-o /Pictures/Flowers/{1}_{0:03d}.jpg".format(nb_ss, filename) # -o, --output    : Output filename <filename> (to write to stdout, use '-o -'). If not specified, no file is saved
#   subprocess.call("raspistill {0} {1} {2} {3}".format(nopreview, shutter, quality, output), shell=True)
   print "ok"
"""
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
#    take_simple_picture(camera, filename)
#    take_corrected_picture(camera, filename)
#    take_5_corrected_pictures(camera, filename)
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
