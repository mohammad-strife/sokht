# product/admin.py
from django.contrib import admin
from .models import GProduct, Product, Order

admin.site.register(GProduct)
admin.site.register(Product)
admin.site.register(Order)
