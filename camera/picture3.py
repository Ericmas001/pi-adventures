#!/usr/bin/python

import subprocess
from datetime import datetime
import sys
from timelapse import timelapse

def startprint( str ):
   sys.stdout.write(str)
   sys.stdout.flush()

def take_picture( nb_ss, filename ):
   startprint( "Taking setting {0} ... ".format(nb_ss))
   nopreview = "-n" # -n, --nopreview : Do not display a preview window
   shutter = "-ss {0}000000".format(nb_ss) # -ss, --shutter  : Set shutter speed in microseconds
   exposure = "-ex backlight" # -ex, --exposure : Set exposure mode (off,auto,night,nightpreview,backlight,spotlight,sports,snow,beach,verylong,fixedfps,antishake,fireworks)
   quality = "-q 100" # -q, --quality   : Set jpeg quality <0 to 100>
   output = "-o /Pictures/tests/{1}_{0:02d}.jpg".format(nb_ss, filename) # -o, --output    : Output filename <filename> (to write to stdout, use '-o -'). If not specified, no file is saved
   subprocess.call("raspistill {0} {1} {2} {3} {4}".format(nopreview, shutter, quality, output, exposure), shell=True)
   print "ok"

filename = datetime.today().strftime("%Y-%m-%d_%H.%M.%S")

print "Taking pictures " + filename + " !!!"

# take_picture(1,filename)
# take_picture(2,filename)
# take_picture(3,filename)
# take_picture(5,filename)
# take_picture(10,filename)
