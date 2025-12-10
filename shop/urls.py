from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("api/indexpost",views.indexpost,name="ShopHomePost"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="Contact"),
    path("tracker/",views.tracker,name="Tracking"),
    path("search/",views.search,name="Search"),
    path("products/<int:myid>/",views.productview,name="ProductView"),
    path("checkout/",views.checkout,name="Checkout")   
]   