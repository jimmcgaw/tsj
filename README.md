# Python, R, & JavaScript Demo

This a small demo project that shows how values loaded into Python can be sent to the R environment, where some data analysis is done, and then values are returned to the Python environment. 

This example uses the Box and Jenkins airline data loaded into Python, R in order to generate a forecast about future data, and JavaScript to plot a chart show both the historical data and future data.

## Hat Tip
This project was build using the [Django Web Framework](https://www.djangoproject.com/), and built using the [Django Project Builder](https://github.com/prototypemagic/django-projectbuilder). A basic understanding on my part of doing time series analysis in R was made possible by the book [Introductory Time Series with R](http://www.amazon.com/dp/0387886974/). 

## Installing
To get this running on your own local machine, you will need Python and R installed. This has been tested on Mac OS X (Lion), with Python 2.7.1 and R version 2.15.2. 

First, clone the source: `git clone git@github.com:smoochy/tsj.git`.

The list of Python packages you need are listed in the requirements.txt file in the root folder of this project. You can install these by using the [pip package manager](https://pypi.python.org/pypi/pip). 

Once you have pip installed, run the following command inside of your project: `pip install -r requirements.txt`. 

This should install all of the listed packages into your Python environment, including rpy2, the Python bindings for the R environment.

## Running
Django comes equipped with a small server you can run locally while in development. 

Inside the root directory of this project, run `python manage.py runserver`.

This will start up the server. You can view the demo in your browser at `http://localhost:8000/`.

## Brain-dead Forecasting in R
Let's do some very simple forecasting in the R environment. Bring up an R shell in your environment of choice and enter the following commands:

```
# create a vector with values 1-36
valueVector <- 1:36
# load the values into a (monthly) timeseries
time_series <- ts(valueVector, freq=12)
# generate the forecast data for next 24 months
hw <- HoltWinters(time_series)
predict(hw, 24)
```