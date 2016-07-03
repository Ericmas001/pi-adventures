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
    Console.WriteLine("ok")
    return my_stream
    
def take_best_picture(camera, filename):
    Console.WriteLine("Taking the best of the best possible picture !!!") 
    
    ideal_brightness = 84
    max_try = 20
    accepted_delta = 2
    
    ss = 2
    count = 0
    delta = 9999.0
    closest_too_much_under_ss = 1
    closest_too_much_under_br = 0
    closest_too_much_under_dt = -1.0
    closest_too_much_over_ss = 1000
    closest_too_much_over_br = 9999
    closest_too_much_over_dt = -1.0
    closest_image = io.BytesIO()
    closest_delta = 9999.0
    
    while(ss > 0 and ss < 1001 and count < max_try and delta > accepted_delta):
        count += 1
        try:
            current_stream = take_picture_stream(camera, int(ss), filename)
            current_brightness = brightness(current_stream)
            delta = abs(ideal_brightness - current_brightness)
            Console.WriteLine("br={0} delta={1} accepted={2}... ok", current_brightness, delta, accepted_delta)
            if(delta < accepted_delta):
                closest_image = current_stream
                closest_delta = delta
                break
                
            if(ss == 1000):
                break
                
            if(current_brightness < ideal_brightness):
                if(closest_too_much_under_br < 0 or current_brightness > closest_too_much_under_br):
                    closest_too_much_under_br = current_brightness
                    closest_too_much_under_ss = ss
                    closest_too_much_under_dt = delta
                
            if(current_brightness > ideal_brightness):
                if(closest_too_much_over_br < 0 or current_brightness < closest_too_much_over_br):
                    closest_too_much_over_br = current_brightness
                    closest_too_much_over_ss = ss
                    closest_too_much_over_dt = delta
                    
            if(closest_too_much_over_dt < 0):
                ss *= 30
            elif(closest_too_much_under_dt < 0):
                ss /= 10
            else:
                pct_under_dt = 100 * closest_too_much_under_dt / (closest_too_much_under_dt + closest_too_much_over_dt)
                if(current_brightness < ideal_brightness):
                    ss += pct_under_dt * (closest_too_much_under_ss + closest_too_much_over_ss) / 100
                else:
                    ss -= (100-pct_under_dt) * (closest_too_much_under_ss + closest_too_much_over_ss) / 100
            
            if(count == max_try):
                break
            
            if(ss > 1000):
                ss = 1000
                count = max_try - 1
                
            if(ss < 1):
                ss = 1
                count = max_try - 1
                
        except Exception as inst:
            Console.WriteLine("")
            print("Unexpected error:", sys.exc_info()[0])    
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst) 
            break;
            
    closest_image.seek(0)
    Console.Write("Accepted delta={0} ... ", closest_delta)
    open("/Pictures/Flowers/{0}_{1:04d}.jpg".format(filename, int(ss)), 'wb').write(closest_image.read())
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
    
    take_best_picture(camera, filename)
    
    pass
finally:
    camera.close()
