from django.contrib import admin

from .models import ProductCategory, Product, ProductMeasure, ProductAttributes, AttributeValue, ProductImage


class AttributesInline(admin.StackedInline):
    model = AttributeValue

    extra = 1


class ProductImageInLine(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [AttributesInline, ProductImageInLine, ]


# admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductMeasure)
admin.site.register(ProductAttributes)
# admin.site.register(AttributeValue)
