
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
ts = r['ts']
HoltWinters = r['HoltWinters']
predict = r['predict']

# magic numbers
MONTHS_TO_PREDICT = 60

def get_historical_data():
	""" 
	load the data from the airline_passengers.csv file and load it into a Python 
	dictionary. The keys are the dates as Python date objects and the values are 
	integers.

	"""
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
	return time_dict, value_vector

def get_series_data():
	""" 
	Grab the historical and forecast dictionaries, and construct a CSV, as a string,
	with the following columns: Date, Historical, Forecast.
	The first rows have historical values and empty forecast values;
	later rows have empty historical values and forecast values.

	"""
	csv = "Date,Historical,Forecast\n"
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
	"""
	Takes a Python list of historical values and the date of the last observation.
	Generate the forecast values for the next MONTHS_TO_PREDICT months and return
	as a Python dictionary, with Python date objects as keys and ints as values.

	"""
	forecast_dict = {}
	# convert Python list to R vector
	value_vector = IntVector(value_vector)
	# create the time series object
	time_series = ts(value_vector, freq=24)
	hw = HoltWinters(time_series)
	forecast = predict(hw, MONTHS_TO_PREDICT)
	# put the future forecast values into a list
	forecast_values = []
	for value in forecast:
		try:
			value = int(value)
		except:
			value = 0
		forecast_values.append(value)
	# future forecast values need dates. Start with last_date, add one month,
	# and take that as first month. Add future months to list below in for loop.
	forecast_months = []
	first_month = last_date + relativedelta.relativedelta(months=1)
	forecast_months.append(first_month)
	current_month = first_month
	for _ in range(1, MONTHS_TO_PREDICT):
		# set current month ahead one month and add it to list
		current_month = current_month + relativedelta.relativedelta(months=1)
		forecast_months.append(current_month)

	# zip the two lists and create a dictionary with dates as keys and values as values
	forecast_zipped = zip(forecast_months, forecast_values)
	for forecast_point in forecast_zipped:
		forecast_dict[forecast_point[0]] = forecast_point[1]
	return forecast_dict

