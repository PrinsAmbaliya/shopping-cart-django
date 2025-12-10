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


urlpatterns = [
    path('admin/', admin.site.urls),
    path("shop/",include("shop.urls")),
    path("blog/",include("blog.urls")),
    path("",views.register,name="Register"),
    path("", lambda request: redirect('/register/')),
    path("login/",views.login_view,name="Login"),
    path("api/registerget", views.api_registerget, name="api_registerget"),
    path("api/registerpost", views.api_registerpost, name="api_registerpost"),
    path("api/registerpatch", views.api_registerpatch, name="api_registerpatch"),
    path("api/{user_id}/registerput", views.api_registerput, name="api_registerput"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)