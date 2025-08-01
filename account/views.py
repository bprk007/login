import re
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect

def is_valid_password(password):
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[^A-Za-z0-9]", password)
    )

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'User with this username already exists')
            return redirect("/auth/register/")
        
        if not is_valid_password(password):
            messages.info(request, 'Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character.')
            return redirect("/auth/register/")

        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()

        messages.info(request, 'User successfully registered, Proceed to login')
        return redirect("/auth/login/")

    template = loader.get_template('register.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login_user(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request,'User with this username does not exist')
            return redirect('/auth/login/')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request,'Invalid Password!')
            return redirect('/auth/login')
        

        login(request,user)
        messages.info(request,'Login successful!')

        return redirect('/auth/login')
    
    template = loader.get_template('login.html')
    context ={}
    return HttpResponse(template.render(context,request))

def logout_user(request):
    logout(request)
    messages.info(request,'logout successful')
    return redirect('/auth/login/')