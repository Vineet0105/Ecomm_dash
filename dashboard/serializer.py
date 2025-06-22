from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'




class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_product  = ProductSerializer()
    order_customer =CustomerSerializer()
    order_platform = PlatformSerializer()

    class Meta:
        model = Order
        fields = '__all__'