#!/usr/bin/python

import os
from datetime import datetime

filename = datetime.today().strftime("%Y-%m-%d")
path_full_logs = "/pics/log.txt"
path_full_new_name = "/pics/log_{0}.txt"
os.rename(path_full_logs,path_full_new_name.format(filename))