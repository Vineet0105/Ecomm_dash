from rest_framework import serializers
from rest_framework.serializers import ValidationError
from .models import *
from django.contrib.auth.models import User
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


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise ValidationError("Account doesn't exists")
        
        return data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError("Account already exists")
        
        return data
    
    def create(self, validated_data):
        user  =User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        return user
    