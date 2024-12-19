from django.db import models

from client.models import CustomUser


# Create your models here.


class GProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=110)
    price = models.IntegerField()
    description = models.TextField()
    deleted = models.BooleanField(default=False)


class Order(models.Model):
    fullname = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=500, blank=True, null=True)
    date = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=100)
    cart = models.BooleanField(default=False)
    amount = models.IntegerField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    farsi = models.CharField(max_length=100, null=True, blank=True)
