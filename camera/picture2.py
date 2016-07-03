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
    
def brightness1( im_file ):
   im = Image.open(im_file).convert('L')
   stat = ImageStat.Stat(im)
   return stat.mean[0]
   
def brightness5( im_file ):
    im = Image.open(im_file)
    stat = ImageStat.Stat(im)
    gs = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)) for r,g,b in im.getdata())
    return sum(gs)/stat.count[0]
    
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
            bright = brightness1(my_stream)
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
    open("/Pictures/tests/{0}_f_{1:04d}.jpg".format(filename, int(ss)), 'wb').write(beststream.read())
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
#    take_picture(camera, 5,filename)
#    take_picture(camera, 10,filename)
#    take_picture(camera, 50,filename)
#    take_picture(camera, 100,filename)
#    take_picture(camera, 200,filename)
#    take_picture(camera, 300,filename)
#    take_picture(camera, 500,filename)
#    take_picture(camera, 1000,filename)
    take_best_picture(camera, filename)
    pass
finally:
    camera.close()
