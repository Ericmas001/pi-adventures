#!/usr/bin/python

import subprocess
from datetime import datetime
import sys

def startprint( str ):
   sys.stdout.write(str)
   sys.stdout.flush()

def take_picture( nb_ss, filename ):
   startprint( "Taking setting {0} ... ".format(nb_ss))
   nopreview = "-n" # -n, --nopreview : Do not display a preview window
   shutter = "-ss {0}00000".format(nb_ss) # -ss, --shutter  : Set shutter speed in microseconds
   quality = "-q 100" # -q, --quality   : Set jpeg quality <0 to 100>
   output = "-o /Pictures/Flowers/{1}_{0:03d}.jpg".format(nb_ss, filename) # -o, --output    : Output filename <filename> (to write to stdout, use '-o -'). If not specified, no file is saved
   subprocess.call("raspistill {0} {1} {2} {3}".format(nopreview, shutter, quality, output), shell=True)
   print "ok"

filename = datetime.today().strftime("%Y-%m-%d_%H.%M.%S")

print "Taking pictures " + filename + " !!!"

take_picture(1,filename)
take_picture(5,filename)
take_picture(10,filename)
take_picture(20,filename)
take_picture(30,filename)
take_picture(50,filename)
take_picture(100,filename)
