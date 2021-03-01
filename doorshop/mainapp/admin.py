from django.contrib import admin

from .models import ProductCategory, Product, ProductMeasure, ProductAttributes

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductMeasure)
admin.site.register(ProductAttributes)
