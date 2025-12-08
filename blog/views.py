from django.shortcuts import render
from django.http import HttpResponse
from . models import Blogpost

# Create your views here.


def index(request):
    mypost = Blogpost.objects.all()
    context = {"mypost":mypost}
    return render(request, "blog/index.html", context)

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id=id).first()
    context = {"post":post}
    return render(request, "blog/blogpost.html",context)