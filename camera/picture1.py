#!/usr/bin/python

import subprocess
from datetime import datetime
import sys

def startprint( str ):
   sys.stdout.write(str)
   sys.stdout.flush()

def take_picture( nb_ss, filename ):
   startprint( "Taking setting {0} ... ".format(nb_ss))
   subprocess.call("raspistill -n -ss {0}000000 -q 100 -o /Pictures/Flowers/{1}_{0:02d}.jpg".format(nb_ss, filename), shell=True)
   print "ok"

filename = datetime.today().strftime("%Y-%m-%d_%H.%M.%S")

print "Taking pictures " + filename + " !!!"

take_picture(1,filename)
take_picture(2,filename)
take_picture(3,filename)
take_picture(5,filename)
take_picture(10,filename)
