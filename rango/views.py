from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category

def index(rqst):
    #loop through cateogries, sorted by likes, and get top 5
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    
    return render(rqst, 'rango/index.html', context=context_dict)

def about(rqst):
    return render(rqst, 'rango/about.html')
