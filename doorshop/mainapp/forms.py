from django import forms
from django.forms import BaseModelFormSet

from mainapp.models import AttributeValue, ProductAttributes


class AttributesForm(forms.ModelForm):
    attribute_id = forms.CharField(max_length=64, disabled=True)
    # attribute_id = forms.CharField(max_length=64)
    value = forms.BooleanField(required=False)

    class Meta:
        model = AttributeValue
        exclude = ('product_id',)

    def __init__(self, *args, **kwargs):
        super(AttributesForm, self).__init__(*args, **kwargs)


class AttributeFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category_id = kwargs.pop('category_id')
        # self.queryset = AttributeValue.objects.filter(attribute_id__category_id_id=kwargs['category_id'])
        self.queryset = AttributeValue.objects.filter(attribute_id__category_id_id=category_id)
        # self.queryset = AttributeValue.objects.all()
