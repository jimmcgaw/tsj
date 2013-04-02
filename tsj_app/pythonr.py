
from datetime import datetime

import csv
import os.path
import sys

# import R stuff
import rpy2.robjects as ro
from rpy2.robjects.vectors import IntVector

# set up some basic R functions here
r = ro.r
c = r['c']
ts = r['ts']
HoltWinters = r['HoltWinters']
predict = r['predict']
unlist = r['unlist']
warnings = r['warnings']
data = r['data']

def load_sample_data():
	""" load the AirPassengers dataset to bootstrap project """
	time_dict = {}
	basepath = os.path.dirname(__file__)
	file_path = os.path.join(basepath, "airline_passengers.csv")
	f = open(file_path, "r") 
	csv_file = csv.reader(f)
	for row in csv_file:
		# convert date string to a Python date object
		date = datetime.strptime(row[0], "%m/%d/%Y") 
		value = row[1]
		time_dict[date] = int(value)
		print date
	return time_dict

