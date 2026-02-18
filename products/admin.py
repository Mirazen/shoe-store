from django.contrib import admin
from .models import Product, Provider, Manufacturer, Category

admin.site.register(Product)
admin.site.register(Provider)
admin.site.register(Manufacturer)
admin.site.register(Category)
