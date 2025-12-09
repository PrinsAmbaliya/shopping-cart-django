from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


# Create your views here.

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        data = User.objects.create_user(username=email,email=email,password=password,first_name=firstname,last_name=lastname)
        data.save()
        return redirect("/shop/")
    return render(request,"register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email,password=password)
        if user:
            login(request, user)
            return redirect("/shop/")
        else:
            messages.error(request,"Invalid email or password")
            return redirect("/login/")
    return render(request, "login.html")