from django.shortcuts import render
from django.http import HttpResponse

def index(rqst):
    return HttpResponse('Rango says hey there partner! <a href="/rango/about/">About</a>')

def about(rqst):
    return HttpResponse('Rango says here is the about page. <a href="/rango/">Index</a>')
