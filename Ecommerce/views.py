from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
import re
import json


@csrf_exempt
@api_view(['GET'])
def api_registerget(request):
    if request.method == "GET":
        users = User.objects.all().values("id", "username", "email", "first_name", "last_name")
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
            return JsonResponse({"error": "Confirm password does not match!"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "This username already exists!"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "This email already exists!"}, status=400)

        User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password,
        )
        return JsonResponse({"message": "User registered successfully"}, status=201)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@api_view(['PUT'])
def api_registerput(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required = ['first_name', 'last_name', 'username', 'email', 'password']
    if not all(field in data and data[field] for field in required):
        return JsonResponse({"error": "All fields are required for PUT"}, status=400)

    if User.objects.exclude(id=user_id).filter(email__iexact=data['email']).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)
    if User.objects.exclude(id=user_id).filter(username__iexact=data['username']).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['username']
    user.email = data['email']
    user.set_password(data['password'])
    user.save()

    return JsonResponse({"message": f"User {user_id} fully updated (PUT)"}, status=200)


@api_view(['PATCH'])
def api_registerpatch(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    try:
        data = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        data = request.POST.dict()

    if 'first_name' in data and data['first_name']:
        user.first_name = data['first_name']
    if 'last_name' in data and data['last_name']:
        user.last_name = data['last_name']
    if 'email' in data and data['email']:
        if User.objects.exclude(id=user_id).filter(email__iexact=data['email']).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)
        user.email = data['email']
    if 'username' in data and data['username']:
        if User.objects.exclude(id=user_id).filter(username__iexact=data['username']).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)
        user.username = data['username']
    if 'password' in data and data['password']:
        user.set_password(data['password'])

    user.save()
    return JsonResponse({
        "message": "User updated successfully (PATCH)",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }, status=200)

@api_view(['DELETE'])
def api_registerdelete(request,user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    user.delete()
    return JsonResponse({"message": f"{user.username} your account is deleted."}, status=200)

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')

        if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[!@#$%^&*()_+\-=\[\]{};'\":\\|,.<>/?]", password):
            messages.error(request, "Password does not meet requirements!")
            return redirect("/")
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("/")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect("/")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("/")

        User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
        return redirect("/shop/")

    return render(request, "register.html")

@api_view(['POST'])
def api_login_viewpost(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        except:
            return JsonResponse({"error": "Invalid username or password"}, status=404   )
    return JsonResponse({"error": "Invalid request method"}, status=405)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/shop/")
        messages.error(request, "Invalid username or password")
        return redirect("/login/")
    return render(request, "login.html")    