from django.shortcuts import render
from django.http import HttpResponse
from . models import Blogpost
from . serializers import BlogpostSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
from django.http import JsonResponse

# Create your views here.


def index(request):
    mypost = Blogpost.objects.all()
    context = {"mypost":mypost}
    return render(request, "blog/index.html", context)

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id=id).first()
    context = {"post":post}
    return render(request, "blog/blogpost.html",context)

class BlogpostCreatAPI(APIView):
    parser_classes = [MultiPartParser,FormParser]
    authentication_classes = []
    def post(self,request,*args, **kwargs):
        serializer = BlogpostSerializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)