from rest_framework import serializers
from . models import Product, Contact, Orders, OrderUpdate

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','product_name','category','subcategory','price','desc','pub_data','image']
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['msg_id','name','email','phone','desc']
        
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['order_id','name','email','address','city','state','zip_code','phone']
        
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderUpdate
        fields = ['update_id','order_id','update_desc','timestamp']