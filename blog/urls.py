from django.contrib import admin
from django.urls import path
from . import views
from . views import BlogpostCreatAPI

urlpatterns = [
    path("",views.index,name="BlogHome"),
    path("blogpost/<int:id>/",views.blogpost,name="BlogPost"),
    path("api/blogpost",BlogpostCreatAPI.as_view(),name="BlogPost"),
]