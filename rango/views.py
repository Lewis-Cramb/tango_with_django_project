from django.shortcuts import render
from django.http import HttpResponse

def index(rqst):
    return HttpResponse("Rango says hey there partner!")
