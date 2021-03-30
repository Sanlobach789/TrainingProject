from django.shortcuts import render

from mainapp.models import ProductCategory, Product, AttributeValue, ProductAttributes


def main(request):
    content = {
        'title': 'Door-Shop'
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'title': 'Doorshop - Товары',
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': Product.objects.filter(is_active=True),
    }
    return render(request, 'mainapp/products.html', content)


def product_detail(request, product_id):
    attribute_values = AttributeValue.objects.filter(product_id=product_id)
    # attribute_name = ProductAttributes.objects.filter(name=attribute_values.attribute_id)
    content = {
        'product': Product.objects.get(id=product_id),
        'attributes': attribute_values,
        # 'attribute_name': attribute_name,
    }
    return render(request, 'mainapp/product-details.html', content)


def get_attributes_values(attribute):
    values_array = []
    attribute_values = AttributeValue.objects.filter(attribute_id=attribute.id)
    for attribute in attribute_values:
        if attribute.value in values_array:
            continue
        else:
            values_array.append(attribute.value)

    return values_array


def get_category_attributes(category_id=None):
    if category_id:
        attributes = ProductAttributes.objects.filter(category_id=category_id)
        attributes_filter = {}
        for attribute in attributes:
            attribute_values = get_attributes_values(attribute)
            attributes_filter[attribute] = attribute_values
        return attributes_filter
    return None


def category_products(request, category_id=None):
    products_list = Product.objects.filter(is_active=True, category=category_id)
    filter_values = get_category_attributes(category_id)
    content = {
        'title': ProductCategory.objects.get(id=category_id).name,
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': products_list,
        'filters': filter_values,
    }
    return render(request, 'mainapp/products.html', content)
