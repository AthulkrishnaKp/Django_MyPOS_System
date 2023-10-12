from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class MyUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'Cashier'),
    )
    role = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=1)
    email = models.EmailField(unique = True)

    def __str__(self):
      return self.username


class Category(models.Model):
    name = models.TextField()
    description = models.TextField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class Products(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    code = models.CharField(max_length=100,unique=True)
    category_id = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    price = models.FloatField(default=50)
    status = models.IntegerField(choices=STATUS_CHOICES,default=1)
    date_added = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.name
        
class SalesItems(models.Model):
    code = models.CharField(default=0,max_length=100,auto_created=True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.PositiveIntegerField(default=0)
    total = models.FloatField(default=0)    
    total_amount = models.FloatField(default=0)
    
class Sales(models.Model):
    sales_items = models.CharField(max_length=200)    
    total_amount = models.FloatField(default=0)
    qty = models.PositiveIntegerField(default=0)
    date_added = models.DateField(auto_now_add=True)