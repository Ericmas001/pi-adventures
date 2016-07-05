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

basepath = "/Pictures/Flowers/{0}_{1:04d}.jpg"
ideal_brightness = 125
max_try = 20
accepted_delta = 2


class Console:
    @staticmethod
    def Write(str, *args):
        sys.stdout.write(str.format(*args))
        sys.stdout.flush()

    @staticmethod
    def WriteLine(str, *args):
        print str.format(*args)
        
    @staticmethod
    def DebugLine(str, *args):
    #    print "DEBUG " + str.format(*args)    
        sys.stdout.flush()
        
class TakenPicture:
    def __init__(self, shutter_speed, img):
        self.img = img
        self.shutter_speed = shutter_speed
        self.brightness = brightness(img)
        self.delta = abs(ideal_brightness - self.brightness)
    
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
    Console.WriteLine("ok")
    return my_stream
    
def take_best_of_the_best_picture(camera, filename):
    Console.WriteLine("Taking the best of the best possible picture !!!") 
        
    current = None
    last = None
    checkpoint = None
    closest = None
    
    ss = 2
    count = 0
    tested_under = False
    tested_over = False
    
    while(ss > 0 and ss < 1001 and count < max_try and (current is None or current.delta > accepted_delta)):
        count += 1
        try:
            current = TakenPicture(ss, take_picture_stream(camera, int(ss), filename))
            Console.WriteLine("br={0} delta={1} accepted={2}", current.brightness, current.delta, accepted_delta)
            
            if current.brightness < ideal_brightness :
                Console.DebugLine("UNDER: CHECK")
                tested_under = True
            
            if current.brightness > ideal_brightness :
                Console.DebugLine("OVER: CHECK")
                tested_over = True
            
            if closest is None or current.delta < closest.delta :
                Console.DebugLine("CLOSEST YET")
                closest = current
                
            if current.delta < accepted_delta :
                Console.DebugLine("OK ! FINISH")
                break
                
            if ss == 1000 and current.brightness < ideal_brightness :
                Console.DebugLine("EXPLODE")
                break

            if ss == 1 and current.brightness > ideal_brightness :
                Console.DebugLine("DIE")
                break
                    
            if not tested_over :
                checkpoint = current
                Console.DebugLine("EXCESSIVE PUSH, CP = CUR")
                ss *= 10
            elif not tested_under :
                checkpoint = current
                Console.DebugLine("EXCESSIVE CALM DOWN, CP = CUR")
                ss /= 10
            else :
                if ss > last.shutter_speed and current.brightness > ideal_brightness :
                    Console.DebugLine("CP = LAST")
                    checkpoint = last
                elif ss < last.shutter_speed and current.brightness < ideal_brightness :
                    Console.DebugLine("CP = LAST")
                    checkpoint = last
                
                pct = 100 * current.delta / (current.delta + checkpoint.delta)
                diff_ss = abs(ss - checkpoint.shutter_speed)
                    
                if current.brightness > ideal_brightness :
                    Console.DebugLine("CONCENTRATE BACKWARD {0:.04f}% of {1}", pct, diff_ss)
                    ss -= pct * (diff_ss) / 100
                else :
                    Console.DebugLine("CONCENTRATE FORWARD {0:.04f}% of {1}", pct)
                    ss += pct * (diff_ss) / 100
            
            if count == max_try :
                Console.DebugLine("ENOUGH")
                break
            
            if ss > 1000 :
                Console.DebugLine("JUST BELOW EXPLOSION")
                ss = 1000
                
            if ss < 1 :
                Console.DebugLine("JUST ABOVE DEATH")
                ss = 1
                
            last = current
            current = None
                
        except Exception as inst :
            Console.WriteLine("")
            print("Unexpected error:", sys.exc_info()[0])    
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst) 
            break;
            
    closest.img.seek(0)
    Console.Write("Accepted delta={0} ... ", closest.delta)
    open(basepath.format(filename, int(closest.shutter_speed)), 'wb').write(closest.img.read())
    Console.WriteLine("saved")
        
filename = datetime.today().strftime("%Y-%m-%d_%H.%M.%S")

Console.WriteLine("Taking pictures {0} !!!", filename)
camera = PiCamera(resolution=(2592, 1944))
try:
   
    camera.iso = 100
    sleep(2)
    camera.exposure_mode = 'off'
  #  g = camera.awb_gains
    camera.awb_mode = 'flash'
  #  camera.awb_gains = g
    
    take_best_of_the_best_picture(camera, filename)
    
    pass
finally:
    camera.close()
