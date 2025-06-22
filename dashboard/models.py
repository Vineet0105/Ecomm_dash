from django.db import models
from uuid import uuid4
from .choices import delivery_choices


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.CharField(unique=True,max_length=255)
    product_name = models.CharField(max_length=255)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product_name

class Customer(models.Model):
    customer_id = models.CharField(unique=True,max_length=255)
    customer_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.customer_name

class Platform(models.Model):
    platform_name = models.CharField(max_length=255)

    def __str__(self):
        return self.platform_name


class Order(models.Model):
    order_id = models.CharField(unique=True,max_length=255)
    order_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_platform = models.ForeignKey(Platform,on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()
    selling_price = models.FloatField()
    sale_date = models.DateField()
    total_sale_value = models.FloatField()
    delviery_address = models.TextField()
    delivery_status = models.CharField(choices=delivery_choices,max_length=100)

    def __str__(self):
        return self.order_id

class FileUpload(models.Model):
    file = models.FileField(upload_to='files')