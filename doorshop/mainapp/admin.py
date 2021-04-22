from django import forms
from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models import ProductCategory, Product, ProductMeasure, ProductAttributes, AttributeValue, ProductImage


class AttributeItemForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        exclude = ('product_id',)

    def __init__(self, *args, **kwargs):
        super(AttributeItemForm, self).__init__(*args, **kwargs)
        product_id = self.instance.product_id
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class AttributesInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(AttributesInlineFormSet, self).__init__(*args, **kwargs)
        # Now we need to make a queryset to each field of each form inline
        self.queryset = AttributeValue.get_category_attributes(self.instance.id)
        print(self.queryset)


class ProductAttributesInLine(admin.StackedInline):
    model = AttributeValue
    formset = AttributesInlineFormSet
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # print(db_field.formfield)
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


admin.site.register(ProductCategory)
admin.site.register(ProductMeasure)
admin.site.register(ProductAttributes)

