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
    
    ideal_brightness = 125
    max_try = 20
    accepted_delta = 2
    
    ss = 2
    count = 0
    delta = 9999.0
    tested_under = False
    tested_over = False
    closest_image = io.BytesIO()
    closest_delta = 9999.0
    closest_ss = 0
    last_dt = -1
    last_br = -1
    last_ss = -1
    
    # TODO: last_last
    # Creation classe pour {dt/br/ss}
    
    while(ss > 0 and ss < 1001 and count < max_try and delta > accepted_delta):
        count += 1
        try:
            current_stream = take_picture_stream(camera, int(ss), filename)
            current_brightness = brightness(current_stream)
            delta = abs(ideal_brightness - current_brightness)
            Console.WriteLine("br={0} delta={1} accepted={2}", current_brightness, delta, accepted_delta)
            
            if current_brightness < ideal_brightness :
                Console.DebugLine("UNDER: CHECK")
                tested_under = True
            
            if current_brightness > ideal_brightness :
                Console.DebugLine("OVER: CHECK")
                tested_over = True
            
            if delta < closest_delta :
                Console.DebugLine("CLOSEST YET")
                closest_image = current_stream
                closest_delta = delta
                closest_ss = ss
                
            if delta < accepted_delta :
                Console.DebugLine("OK")
                break
                
            if ss == 1000 and current_brightness < ideal_brightness :
                Console.DebugLine("EXPLODE")
                break

            if ss == 1 and current_brightness > ideal_brightness :
                Console.DebugLine("DIE")
                break
                    
            if not tested_over :
                last_ss = ss
                Console.DebugLine("EXCESSIVE PUSH")
                ss *= 10
            elif not tested_under :
                last_ss = ss
                Console.DebugLine("EXCESSIVE CALM DOWN")
                ss /= 10
            else :
                if ss > last_ss and current_brightness < ideal_brightness :
                    diff_ss = ss - last_ss
                    last_ss = ss
                    Console.DebugLine("NOT ENOUGH ++")
                    ss += diff_ss
                elif ss < last_ss and current_brightness > ideal_brightness :
                    diff_ss = last_ss - ss
                    last_ss = ss
                    Console.DebugLine("NOT ENOUGH --")
                    ss -= diff_ss
                elif ss > last_ss :
                    diff_ss = ss - last_ss
                    last_ss = ss
                    pct = 100 * delta / (delta + last_dt)
                    Console.DebugLine("CONCENTRATE BACKWARD {0:.04f}%", pct)
                    ss -= pct * (diff_ss) / 100
                else :
                    diff_ss = last_ss - ss
                    last_ss = ss
                    pct = 100 * delta / (delta + last_dt)
                    Console.DebugLine("CONCENTRATE FORWARD {0:.04f}%", pct)
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
            last_dt = delta
            last_br = current_brightness
                
        except Exception as inst :
            Console.WriteLine("")
            print("Unexpected error:", sys.exc_info()[0])    
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst) 
            break;
            
    closest_image.seek(0)
    Console.Write("Accepted delta={0} ... ", closest_delta)
    open(basepath.format(filename, int(ss)), 'wb').write(closest_image.read())
    Console.WriteLine("saved")
        
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
    
    take_best_of_the_best_picture(camera, filename)
    
    pass
finally:
    camera.close()
