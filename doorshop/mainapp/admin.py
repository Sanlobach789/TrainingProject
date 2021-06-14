from django.contrib import admin

from .models import ProductCategory, Product, ProductMeasure, ProductAttributes, AttributeValue, ProductImage, \
    SortValues, SocialUrls


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
    list_filter = ('category_id',)


@admin.register(ProductCategory)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_category')
    list_filter = ('is_parent_category',)


admin.site.register(ProductMeasure)
admin.site.register(SortValues)
admin.site.register(SocialUrls)
