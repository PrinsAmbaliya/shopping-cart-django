from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import re
import json


class UserRegistrationAPI(APIView):
    authentication_classes = [] 

    def get(self, request, user_id=None, *args, **kwargs):
        if user_id:
            try:
                user = User.objects.filter(id=user_id).values("id", "username", "email", "first_name", "last_name").first()
                if user:
                    return Response(user, status=status.HTTP_200_OK)
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                return Response({"error": "Invalid user ID format"}, status=status.HTTP_400_BAD_REQUEST)
        
        users = User.objects.all().values("id", "username", "email", "first_name", "last_name")
        return Response(list(users), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data 
        
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        username = data.get('username')
        email = data.get('email')
        firstname = data.get('first_name')
        lastname = data.get('last_name')

        if len(password) < 8:
            return Response({"error": "Password must be 8+ characters!"}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r"[A-Z]", password):
            return Response({"error": "Password must have one UPPER character!"}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r"[a-z]", password):
            return Response({"error": "Password must have one LOWER character!"}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r"[0-9]", password):
            return Response({"error": "Password must have one NUMBER!"}, status=status.HTTP_400_BAD_REQUEST)
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};'\":\\|,.<>/?]", password):
            return Response({"error": "Password must have one SPECIAL character!"}, status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response({"error": "Confirm password does not match!"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "This username already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "This email already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password,
        )
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

    def put(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        required = ['first_name', 'last_name', 'username', 'email', 'password']
        if not all(field in data and data.get(field) for field in required):
             return Response({"error": "All fields are required for PUT"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.exclude(id=user_id).filter(email__iexact=data['email']).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.exclude(id=user_id).filter(username__iexact=data['username']).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.username = data['username']
        user.email = data['email']
        user.set_password(data['password'])
        user.save()

        return Response({"message": f"User {user_id} fully updated (PUT)"}, status=status.HTTP_200_OK)

    def patch(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        
        if 'first_name' in data and data['first_name']:
            user.first_name = data['first_name']
        if 'last_name' in data and data['last_name']:
            user.last_name = data['last_name']
        if 'email' in data and data['email']:
            if User.objects.exclude(id=user_id).filter(email__iexact=data['email']).exists():
                return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user.email = data['email']
        if 'username' in data and data['username']:
            if User.objects.exclude(id=user_id).filter(username__iexact=data['username']).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
            user.username = data['username']
        if 'password' in data and data['password']:
            user.set_password(data['password'])

        user.save()
        return Response({
            "message": "User updated successfully (PATCH)",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }, status=status.HTTP_200_OK)

    def delete(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": f"{user.username} your account is deleted."}, status=status.HTTP_200_OK)


class UserLoginCreateAPI(APIView):
    authentication_classes = []
    def post(self,request,*args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                 return JsonResponse({"error": "Invalid username or password"}, status=401)
        except Exception:
             return JsonResponse({"error": "Invalid username or password"}, status=401)

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