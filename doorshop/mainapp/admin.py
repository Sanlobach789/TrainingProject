from django.contrib import admin

from .models import ProductCategory, Product, ProductMeasure, ProductAttributes, AttributeValue, ProductImage, \
    SortValues


class ProductAttributesInLine(admin.StackedInline):
    model = AttributeValue
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'attribute_id':
            parent_id = request.resolver_match.kwargs['object_id']
            kwargs['queryset'] = AttributeValue.get_category_attributes(product_id=parent_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductImageInLine(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    inlines = [ProductAttributesInLine, ProductImageInLine, ]


@admin.register(ProductAttributes)
class AttributesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_id')


admin.site.register(ProductCategory)
admin.site.register(ProductMeasure)
admin.site.register(SortValues)
