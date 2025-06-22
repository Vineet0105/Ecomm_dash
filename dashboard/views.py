import os
from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from .serializer import *
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from .file_reader import *
from pathlib import Path
from .rate_limiter import rate_limit
from utils.paginate import *
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from .permission import *
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    pagination_class = LargeResultPagination
    authentication_classes = [TokenAuthentication]
    permission_classes =  [IsUser]

class OrderAPI(APIView):
    @rate_limit(max_requests=10,time_window=60*2)
    def get(self,request):
        query_set = Order.objects.all().order_by('id')
        paginator = LargeResultPagination()
        paginated_query= paginator.paginate_queryset(query_set,request)
        serializer = OrderSerializer(paginated_query,many=True)

        return Response(
            paginator.get_paginated_response(serializer.data).data
        ,status.HTTP_200_OK)

   
class CustomerAPI(APIView):
    @rate_limit(max_requests=10,time_window=60*2)
    def get(self,request):
        query_set = Customer.objects.all()
        serializer = CustomerSerializer(query_set,many=True)
        return Response({
            'Status':'True',
            'Message':'Ran',
            'Data':serializer.data,
        },status.HTTP_200_OK)
    
class ProductAPI(APIView):
    @rate_limit(max_requests=10,time_window=60*2)
    def get(self,request):
        query_set = Product.objects.all()
        page_number = request.GET.get('page',1)
        paginator = Paginator(query_set,100)
        data = paginate(query_set,paginator,page_number)
        serializer = ProductSerializer(data['result'],many=True)
        data['result'] = serializer.data
        return Response(data,status.HTTP_200_OK)

class FileUploadAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsUser]
    @rate_limit(max_requests=10,time_window=60*2)
    def post(self,request):
        data =request.data
        serializer = FileUploadSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'Status':'False',
                'Message':'Got an Error',
                'Error':serializer.errors,
            },status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()
        read_file(instance.file.path)
        return Response({
            'Status':'True',
            'Message':'File Uploaded',
        },status.HTTP_201_CREATED)
    

class LoginAPI(APIView):
    def get(self,request):
        data = request.data
        serializer= LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'Status':'False',
                'Message':'Got an Error',
                'Error':serializer.errors,
            },status.HTTP_400_BAD_REQUEST)

        user = authenticate(username = data['username'],password=data['password'])
        if user is None:
            return Response({
                'Status':'False',
                'Message':'Invalid Password',
            },status.HTTP_400_BAD_REQUEST)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'Status':'True',
            'Message':'login Successful',
            'Token': str(token)
        },status.HTTP_200_OK)
    

class RegisterAPI(APIView):
    def post(self,request):
        data = request.data
        serializer= RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'Status':'False',
                'Message':'Got an Error',
                'Error':serializer.errors,
            },status.HTTP_400_BAD_REQUEST)

        serializer.save()
        user = authenticate(username = data['username'],password=data['password'])        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'Status':'True',
            'Message':'Creation Successful',
            'Token': str(token)
        },status.HTTP_201_CREATED)