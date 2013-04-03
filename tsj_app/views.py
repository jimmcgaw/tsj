from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render, \
    redirect
from django.template import loader, RequestContext
from django.views.decorators.csrf import csrf_exempt

from tsj_app.models import *
from tsj_app.model_forms import *
from tsj_app.forms import *
from tsj_app import pythonr


import simplejson

def index(request, template_name="index.html"):
    return render(request, template_name, locals())

def get_data(request):
	data = {}
	data["csv"] = pythonr.get_series_data()
	json = simplejson.dumps(data)
	return HttpResponse(json, content_type="application/json")