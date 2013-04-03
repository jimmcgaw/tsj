
from datetime import datetime
from dateutil import relativedelta

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

# magic numbers
MONTHS_TO_PREDICT = 60

def get_historical_data():
	""" load the AirPassengers dataset to bootstrap project """
	time_dict = {}
	value_vector = []
	basepath = os.path.dirname(__file__)
	file_path = os.path.join(basepath, "airline_passengers.csv")
	f = open(file_path, "r") 
	csv_file = csv.reader(f)
	for row in csv_file:
		# convert date string to a Python date object
		date = datetime.strptime(row[0], "%m/%d/%Y") 
		value = row[1]
		time_dict[date] = int(value)
		value_vector.append(value)
		print date
	return time_dict, value_vector

def get_series_data():
	""" grab dictionary and build csv as string """
	csv = "Date,Value,Forecast\n"
	historical_dict, value_vector = get_historical_data()
	# build the historical data portion of the CSV
	for key, value in historical_dict.iteritems():
		csv += key.strftime("%Y-%m-%d")
		csv += ","
		csv += str(value)
		csv += ",\n"

	last_date = max(historical_dict.keys())

	forecast_dict = get_forecast_data(value_vector, last_date)

	for date, value in forecast_dict.iteritems():
		#print date
		csv += date.strftime("%Y-%m-%d")
		csv += ",,"
		csv += str(value)
		csv += "\n"

	return csv

def get_forecast_data(value_vector, last_date):
	print last_date
	forecast_dict = {}
	value_vector = IntVector(value_vector)
	time_series = ts(value_vector, freq=24)
	hw = HoltWinters(time_series)
	forecast = predict(hw, MONTHS_TO_PREDICT)
	forecast_values = []
	for value in forecast:
		try:
			value = int(value)
		except:
			value = 0
		forecast_values.append(value)

	forecast_months = []
	first_month = last_date + relativedelta.relativedelta(months=1)
	forecast_months.append(first_month)
	current_month = first_month
	for _ in range(1, MONTHS_TO_PREDICT):
		current_month = current_month + relativedelta.relativedelta(months=1)
		forecast_months.append(current_month)

	forecast_zipped = zip(forecast_months, forecast_values)
	for forecast_point in forecast_zipped:
		forecast_dict[forecast_point[0]] = forecast_point[1]
	return forecast_dict

