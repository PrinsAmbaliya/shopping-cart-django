from django.contrib import admin
from . models import Product,Contact,Orders,OrderUpdate


# Register your models here.
class Productadmin(admin.ModelAdmin):
    list_display=(
        'id',
        'product_name',
        'category',
        'subcategory',
        'price',
        'pub_data'
    )
    list_filter = ('category','subcategory')
    search_fields = ('product_name','desc','id')
admin.site.register(Product, Productadmin)

class Contactadmin(admin.ModelAdmin):
    list_display=(
        'msg_id',
        'name',
        'email',
        'phone'
    )
    list_filter = ()
    search_fields = ('name','email','phone','msg_id')
admin.site.register(Contact,Contactadmin)

class Ordersadmin(admin.ModelAdmin):
    list_display=(
        'order_id',
        'name',
        'email',
        'city',
        'state',
        'amount',
        'phone'
    )
    list_filter=('city','state')
    search_fields = ('name','email','phone','order_id')
admin.site.register(Orders,Ordersadmin)


class OrderUpdateadmin(admin.ModelAdmin):
    list_display=(
        'update_id',
        'order_id',
        'timestamp'
    )
    list_filter=()
    search_fields=('order_id','timestamp')
admin.site.register(OrderUpdate,OrderUpdateadmin)