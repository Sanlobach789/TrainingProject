from django import forms
from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import ProductCategory, Product, ProductMeasure, ProductAttributes, AttributeValue, ProductImage


class AttributesInlineFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(AttributesInlineFormSet, self).__init__(*args, **kwargs)
        # Now we need to make a queryset to each field of each form inline
        self.queryset = AttributeValue.get_category_attributes(self.instance.id)


# class AttributesForm(forms.ModelForm):
#     class Meta:
#         model = AttributeValue
#         fields = ('attribute_id', 'value')
#
#
#     def __init__(self, *args, **kwargs):
#         super(AttributesForm, self).__init__(*args, **kwargs)
#         self.fields['attribute_id'].initial =


class ProductAttributesInLine(admin.StackedInline):
    model = AttributeValue
    formset = AttributesInlineFormSet
    extra = 0


class ProductImageInLine(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductAttributesInLine, ProductImageInLine, ]


admin.site.register(ProductCategory)
admin.site.register(ProductMeasure)
admin.site.register(ProductAttributes)

