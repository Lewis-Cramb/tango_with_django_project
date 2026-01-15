from django.shortcuts import render
from django.http import HttpResponse

def index(rqst):
    #Construct dict to pass template engine as context
    #boldmessage matches to {{boldmessage}}
    context_dict = {'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}

    #return rendered repsonse
    #shortcut function
    #first param is template to use
    return render(rqst, 'rango/index.html', context=context_dict)

def about(rqst):
    return HttpResponse('Rango says here is the about page. <a href="/rango/">Index</a>')
