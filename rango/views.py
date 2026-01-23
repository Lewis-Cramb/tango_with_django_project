from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse

def index(rqst):
    #loop through cateogries, sorted by likes, and get top 5
    category_list = Category.objects.order_by('-likes')[:5]
    #loop through pages, sorted by views, and get top 5
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    
    return render(rqst, 'rango/index.html', context=context_dict)

def about(rqst):
    return render(rqst, 'rango/about.html')

def show_category(rqst,category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(rqst, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form':form})

def add_page(rqst, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    if rqst.method =="POST":
        form = PageForm(rqst.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.url = form.cleaned_data['url']
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form':form, 'category':category}
    return render(rqst, 'rango/add_page.html', context=context_dict)