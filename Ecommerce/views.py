from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import User
from django.core import serializers     
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
import re

# Create your views here.
@csrf_exempt
def api_registerget(request):
    if request.method == "GET":
        users = User.objects.all().values("id", "username", "email", "first_name", "last_name","password")
        return JsonResponse(list(users), safe=False)
    return JsonResponse({"error": "Invalid method"}, status=405)


@api_view(['POST'])
def api_registerpost(request):
    if request.method == "POST":
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')  
        confirm_password = request.POST.get('confirm_password') 
        
        if len(password) < 8:
            return JsonResponse({"error": "Password must be 8+ characters!"}, status=400)

        if not re.search(r"[A-Z]", password):
            return JsonResponse({"error": "Password must have one UPPER character!"}, status=400)

        if not re.search(r"[a-z]", password):
            return JsonResponse({"error": "Password must have one LOWER character!"}, status=400)

        if not re.search(r"[0-9]", password):
            return JsonResponse({"error": "Password must have one NUMBER!"}, status=400)

        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};'\":\\|,.<>/?]", password):
            return JsonResponse({"error": "Password must have one SPECIAL character!"}, status=400)
        
        if password != confirm_password:
            return JsonResponse({"error": "Confirm password is not match with password!"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "This username already exists!"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "This email already exists!"}, status=400)

        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password,
        )

        return JsonResponse({
            "message": "User registered successfully",
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "email": email,
            "password": password
        }, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405) 

@api_view(['PATCH'])
def api_registerpatch(request, user_id): 
    if request.method == "PATCH":
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = JsonResponse.loads(request.body.decode("utf-8"))
        except JsonResponse.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
            
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        
        if "email" in data:
            if User.objects.exclude(id=user_id).filter(email=data["email"]).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)
            user.email = data["email"]
            
        if "username" in data:
            if User.objects.exclude(id=user_id).filter(username=data["username"]).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            user.username = data["username"]

        user.save()

        return JsonResponse({"message": "User partially updated"})
    

@api_view(['PUT'])
def api_registerput(request, user_id):
    if request.method == "PUT":
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = JsonResponse.loads(request.body.decode("utf-8"))
        except JsonResponse.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        required_fields = ["first_name", "last_name", "email", "username"]
        if not all(field in data for field in required_fields):
            return JsonResponse({"error": f"Missing required fields for PUT: {', '.join(required_fields)}"}, status=400)

        if User.objects.exclude(id=user_id).filter(email=data["email"]).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)
        if User.objects.exclude(id=user_id).filter(username=data["username"]).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.username = data["username"]

        user.save()
        return JsonResponse({"message": "User fully updated"})
    
def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')  
        confirm_password = request.POST.get('password2')
        

        if len(password) < 8:
            messages.error(request,"Password must be 8+ charter!")
            return redirect("/")
        if not re.search(r"[A-Z]",password):
            messages.error(request,"In Password must be once UPPER charter!")
            return redirect("/")            
        if not re.search(r"[a-z]",password):
            messages.error(request,"In Password must be once lower charter!")
            return redirect("/")
        if not re.search(r"[0-9]",password):
            messages.error(request,"In Password must be One Number!")
            return redirect("/")
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]",password):
            messages.error(request,"In Password must be One Special charter!")
            return redirect("/")
        if password != confirm_password:
            messages.error(request,"Confirm password is not match with password!")      
            return redirect("/")
        if User.objects.filter(username=username).exists():
            messages.error(request,"This username aleady exits!")
            return redirect("/")
        if User.objects.filter(email=email).exists():
            messages.error(request,"This email already exits!")
            return redirect("/")
        
        data = User.objects.create_user(username=username,email=email,password=password,first_name=firstname,last_name=lastname)
        data.save()
        return redirect("/shop/")
    
    return render(request,"register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request, user)
            return redirect("/shop/")
        else:
            messages.error(request,"Invalid email or password")
            return redirect("/login/")
    return render(request, "login.html")