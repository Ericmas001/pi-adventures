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
import json
import os
import traceback
from fractions import Fraction
import requests

washer_key = "Washer"
dryer_key = "Dryer"
misc_key = "GeneralConfig"

path_full_photo = "/pics/{0}_{1:04d}_{2:02d}_{3}.jpg"
path_washer = "/pics/washer_{0}.jpg"
path_dryer = "/pics/dryer_{0}.jpg"
ideal_brightness = 10
max_try = 20
accepted_delta = 1
path_full_photo_config = "/pics/last_config.json"
config = None


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
        
class PictureConfig:
    def __init__(self, shutter_speed, brightness, delta, filename):
        self.shutter_speed = shutter_speed
        self.brightness = brightness
        self.delta = delta
        self.filename = filename
    
def brightness( im_file ):
   im = Image.open(im_file).convert('L')
   mini_washer = im.crop((int(config[washer_key]["Left"]) + int(config[washer_key]["LeftStudy"]), int(config[washer_key]["Top"]) + int(config[washer_key]["TopStudy"]), int(config[washer_key]["Left"]) + int(config[washer_key]["RightStudy"]), int(config[washer_key]["Top"]) + int(config[washer_key]["BottomStudy"])))
   mini_dryer = im.crop((int(config[dryer_key]["Left"]) + int(config[dryer_key]["LeftStudy"]), int(config[dryer_key]["Top"]) + int(config[dryer_key]["TopStudy"]), int(config[dryer_key]["Left"]) + int(config[dryer_key]["RightStudy"]), int(config[dryer_key]["Top"]) + int(config[dryer_key]["BottomStudy"])))
   stat_washer = ImageStat.Stat(mini_washer)
   stat_dryer = ImageStat.Stat(mini_dryer)
   return max(stat_washer.mean[0],stat_dryer.mean[0])
    
def take_picture_stream(camera, nb_ss, filename):
    Console.Write("Taking stream, setting #{0} ... ", nb_ss) 
    my_stream = io.BytesIO()
    camera.framerate = float((float(101) - (float(nb_ss) / float(100))) / float(100))
    camera.shutter_speed = 1000 * nb_ss
    Console.Write("ss={0}, awb={1} ... ",camera.shutter_speed,camera.awb_mode)
    camera.capture(my_stream, 'jpeg')
    my_stream.seek(0)
    Console.WriteLine("ok")
    return my_stream
    
def take_best_picture_remembering(camera, last_photoshoot, filename):
    Console.WriteLine("Taking the best of the best possible picture !!!") 
        
    current = None
    last = None
    checkpoint = None
    closest = None
    
    ss = 2 if last_photoshoot is None else last_photoshoot.shutter_speed
    count = 0
    tested_under = False
    tested_over = False
    stopped_reason = "unknown"
    
    while(ss > 0 and ss < 10001 and count < max_try and (current is None or current.delta > accepted_delta)):
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
                stopped_reason = "accepted"
                break
                
            if ss == 10000 and current.brightness < ideal_brightness :
                Console.DebugLine("EXPLODE")
                stopped_reason = "max_ss"
                break

            if ss == 1 and current.brightness > ideal_brightness :
                stopped_reason = "min_ss"
                Console.DebugLine("DIE")
                break
                    
            if not tested_over :
                checkpoint = current
                multiplier = min(10, max(2, current.delta / 10))
                Console.DebugLine("EXCESSIVE PUSH * {0}, CP = CUR", multiplier)
                ss *= multiplier
            elif not tested_under :
                checkpoint = current
                divider = min(10, max(2, current.delta / 10))
                Console.DebugLine("EXCESSIVE CALM DOWN / {0}, CP = CUR", divider)
                ss /= divider
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
                    Console.DebugLine("CONCENTRATE FORWARD {0:.04f}% of {1}", pct, diff_ss)
                    ss += pct * (diff_ss) / 100
            
            if count == max_try :
                Console.DebugLine("ENOUGH")
                stopped_reason = "max_tries"
                break
            
            if ss > 10000 :
                Console.DebugLine("JUST BELOW EXPLOSION")
                ss = 10000
                
            if ss < 1 :
                Console.DebugLine("JUST ABOVE DEATH")
                ss = 1
            
            if int(ss) == int(current.shutter_speed) :
                stopped_reason = "closest"
                break;
                
            last = current
            current = None
                
        except Exception as inst :
            Console.WriteLine("")
            print("Unexpected error:", sys.exc_info()[0])    
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst) 
            traceback.print_exc()
            break;
            
    current.img.seek(0)
    Console.WriteLine("Finished because {0} ", stopped_reason)
    full_image_path = "NOT SAVED"
    full_image_path = path_full_photo.format(filename, int(current.shutter_speed), count, stopped_reason)
    open(full_image_path, 'wb').write(current.img.read())
    Console.WriteLine("saved")
    current.img.seek(0)
    img = Image.open(current.img)
    path_washer_final = path_washer.format(filename)
    path_dryer_final = path_dryer.format(filename)
    img.crop((int(config[washer_key]["Left"]), int(config[washer_key]["Top"]), int(config[washer_key]["Right"]), int(config[washer_key]["Bottom"]))).save(path_washer_final)
    img.crop((int(config[dryer_key]["Left"]), int(config[dryer_key]["Top"]), int(config[dryer_key]["Right"]), int(config[dryer_key]["Bottom"]))).save(path_dryer_final)
    url = 'http://washerdryerwebservice.azurewebsites.net/api/upload'
    files = {"form_input_field_name1": open(path_washer_final, "rb"),"form_input_field_name2": open(path_dryer_final, "rb")}
    requests.post(url, files=files)
    cfg = open(path_full_photo_config, "w")
    cfg.write(json.dumps({'shutter_speed': current.shutter_speed, 'brightness': current.brightness, 'delta': current.delta, 'filename': full_image_path, 'stopped_reason': stopped_reason}, sort_keys=True,indent=4, separators=(',', ': ')))
    cfg.close()
    os.remove(path_washer_final)
    os.remove(path_dryer_final)
	
Console.WriteLine("===============================================================================")
try:    
	camera = PiCamera(resolution=(2592, 1944))    
	try:
		filename = datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
		Console.WriteLine("Taking pictures {0} !!!", filename)

		last_photoshoot = None
		if os.path.isfile(path_full_photo_config) :
			with open(path_full_photo_config, 'r') as content_file :
				j = json.loads(content_file.read())
				last_photoshoot = PictureConfig(j["shutter_speed"], j["brightness"], j["delta"], j["filename"])
	   
		url = 'http://washerdryerwebservice.azurewebsites.net/api/config'
		config = requests.get(url).json()
		
		ideal_brightness = int(config[misc_key]["IdealBrightness"])
		max_try = int(config[misc_key]["MaxTry"])
		accepted_delta = float(config[misc_key]["AcceptedDelta"])
		camera.iso = 100
        camera.rotation = 90
		camera.exposure_mode = 'off'
		camera.awb_mode = 'off'
		camera.exposure_mode = 'off'
		camera.drc_strength='off'
		camera.awb_gains = (Fraction(753,557),Fraction(753,557))
		sleep(2)
		take_best_picture_remembering(camera,last_photoshoot,filename)
		
		pass
		
					
	except Exception as inst :
		Console.WriteLine("")
		print("Unexpected error:", sys.exc_info()[0])    
		print(type(inst))    # the exception instance
		print(inst.args)     # arguments stored in .args
		print(inst) 
		traceback.print_exc()
	finally:
		camera.close()
except Exception as inst :
    Console.WriteLine(">>>>>   C A M E R A    I S    B U S Y   <<<<<")
