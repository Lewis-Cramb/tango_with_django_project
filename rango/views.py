from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

def add_category(rqst):
    form = CategoryForm()
    if rqst.method == "POST":
        form = CategoryForm(rqst.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(rqst, 'rango/add_category.html', {'form':form})

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


def register(rqst):
    registered = False
    if rqst.method == 'POST':
        user_form = UserForm(rqst.POST)
        profile_form = UserProfileForm(rqst.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) #hashes pw
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in rqst.FILES:
                profile.picture = rqst.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(rqst, 'rango/register.html', context={'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(rqst):
    if rqst.method == 'POST':
        username = rqst.POST.get('username')
        password = rqst.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(rqst, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(rqst, 'rango/login.html')
    

@login_required()
def restricted(rqst):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required()
def user_logout(rqst):
    logout(rqst)
    return redirect(reverse('rango:index'))