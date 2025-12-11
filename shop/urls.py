from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from . import views
from .views import ProductCreateAPI, ContactCreatAPI, OrdersCreatAPI, OrderUpdateCreatAPI

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("api/indexpost", ProductCreateAPI.as_view(), name="ShopHomePost"),
    path("about/",views.about,name="AboutUs"),
    path("contact/",views.contact,name="Contact"),
    path("api/contactpost", ContactCreatAPI.as_view(),name="ContactPost"),
    path("tracker/",views.tracker,name="Tracking"),
    path("search/",views.search,name="Search"),
    path("products/<int:myid>/",views.productview,name="ProductView"),
    path("checkout/",views.checkout,name="Checkout"),
    path("api/orderpost",OrdersCreatAPI.as_view(),name="CheckoutPost"),
    path("api/orderupdatepost",OrderUpdateCreatAPI.as_view(),name="CheckoutPost"),
]   