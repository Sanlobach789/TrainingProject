from django.contrib import admin

from .models import ProductCategory, Product, ProductMeasure, ProductAttributes, AttributeValue


class AttributesInline(admin.StackedInline):
    model = AttributeValue


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [AttributesInline, ]


# admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductMeasure)
admin.site.register(ProductAttributes)
# admin.site.register(AttributeValue)
