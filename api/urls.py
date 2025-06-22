from django.contrib import admin
from django.urls import path,include
from dashboard.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('customers',CustomerViewset,basename='customers')

urlpatterns = [
    path('', include(router.urls)),
    path('file/',FileUploadAPI.as_view()),
    path('order/',OrderAPI.as_view()),
    path('customer/',CustomerAPI.as_view()),
    path('product/',ProductAPI.as_view()),
]