"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from . import views
from . views import UserRegistrationAPI, UserLoginCreateAPI


urlpatterns = [
    path('admin/', admin.site.urls),
    path("shop/",include("shop.urls")),
    path("blog/",include("blog.urls")),
    path("",views.register,name="Register"),
    path("login/",views.login_view,name="Login"),
    path("api/loginpost",UserLoginCreateAPI.as_view(),name="api_Loginpost"),
    path("api/registerget", UserRegistrationAPI.as_view(), name="api_registerget"),
    path("api/registerpost", UserRegistrationAPI.as_view(), name="api_registerpost"),
    path("api/<int:user_id>/registerpatch", UserRegistrationAPI.as_view(), name="api_registerpatch"),
    path("api/<int:user_id>/registerput", UserRegistrationAPI.as_view(), name="api_registerput"),
    path("api/<int:user_id>/registerdelete", UserRegistrationAPI.as_view(),name="api_registerdelete"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)