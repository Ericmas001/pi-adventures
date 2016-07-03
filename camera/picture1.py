#!/usr/bin/python

import subprocess
from datetime import datetime
import sys

def startprint( str ):
   sys.stdout.write(str)
   sys.stdout.flush()

filename = datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
print "Taking pictures " + filename + " !!!"
startprint( "Taking setting 1 ... ")
subprocess.call("raspistill -n -ss 1000000 -q 100 -o /Pictures/%s_01.jpg" % (filename), shell=True)
print "ok"
startprint( "Taking setting 2 ... ")
subprocess.call("raspistill -n -ss 2000000 -q 100 -o /Pictures/%s_02.jpg" % (filename), shell=True)
print "ok"
startprint( "Taking setting 3 ... ")
subprocess.call("raspistill -n -ss 3000000 -q 100 -o /Pictures/%s_03.jpg" % (filename), shell=True)
print "ok"
startprint( "Taking setting 5 ... ")
subprocess.call("raspistill -n -ss 5000000 -q 100 -o /Pictures/%s_05.jpg" % (filename), shell=True)
print "ok"
startprint( "Taking setting 10 ... ")
subprocess.call("raspistill -n -ss 10000000 -q 100 -o /Pictures/%s_10.jpg" % (filename), shell=True)
print "ok"

