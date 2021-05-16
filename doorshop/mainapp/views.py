from django.forms import modelform_factory, modelformset_factory
from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from mainapp.forms import AttributeFormSet, AttributesForm
from mainapp.models import ProductCategory, Product, AttributeValue, ProductAttributes
from mainapp.serializers import product_list_serializer


def main(request):
    content = {
        'title': 'Door-Shop'
    }
    return render(request, 'mainapp/index.html', content)


def products_index(request):
    try:
        data = request.GET['search']
        items = Product.objects.filter(name__contains=data.title())
        items = items | Product.objects.filter(name__contains=data.lower())
        product_list = items
    except MultiValueDictKeyError:
        product_list = Product.objects.filter(is_active=True)

    content = {
        'title': 'Doorshop - Товары',
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': product_list
    }
    return render(request, 'mainapp/products.html', content)


def product_detail(request, product_id):
    attribute_values = AttributeValue.objects.filter(product_id=product_id)
    product = Product.objects.get(id=product_id)
    images = product.images.all()
    content = {
        'title': product.name,
        'product': product,
        'attributes': attribute_values,
        'product_images': images,
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


# Функционал фильтрации_________________________________________________
def get_price_filter(product_list):
    if len(product_list) > 1:
        min_price_product = product_list.order_by('price')[0],
        max_price_product = product_list.order_by('-price')[0],
        min = float(min_price_product[0].get_price())
        max = float(max_price_product[0].get_price())
        price_filter = {
            "min": int(round(min)),
            "max": int(round(max)),
        }
    else:
        price_filter = None

    return price_filter


def simple_filter(attr_id, values, founded_products=None):
    result = AttributeValue.objects.none()
    if not founded_products:
        for val in values:
            buffer = AttributeValue.objects.filter(attribute_id=attr_id, value=val)
            result = result | buffer
        return result
    else:
        for item in founded_products.values('product_id'):
            for val in values:
                buffer = AttributeValue.objects.filter(
                    attribute_id_id=attr_id,
                    product_id_id=item['product_id'],
                    value=val
                )
                result = result | buffer
        return result


def recurs_filter(filter_set, founded_products=None, counter=0):
    len_of_filters = len(filter_set)
    if counter > len_of_filters:
        # founded_products = product_list_serializer(founded_products)
        return founded_products
    else:
        for key, values in filter_set.items():
            if founded_products:
                founded_products = simple_filter(attr_id=key, values=values, founded_products=founded_products)
                new_filter_set = filter_set.copy()
                new_filter_set.pop(key)
                counter += 1
                return recurs_filter(new_filter_set, founded_products, counter)
            else:
                founded_products = simple_filter(attr_id=key, values=values)
                new_filter_set = filter_set.copy()
                new_filter_set.pop(key)
                counter += 1
                return recurs_filter(new_filter_set, founded_products, counter)


def create_filterset(filter_dict):
    filter_set = {}
    price_set = {}
    for key, value in filter_dict:
        if key.isdigit():
            filter_set[key] = value
        elif key == 'min_price':
            price_set['min'] = int(value[0])
        elif key == 'max_price':
            price_set['max'] = int(value[0])
    return {'attribute_filter': filter_set, 'price_filter': price_set}


def price_filtered_products(product_list, price_range):
    min_price = price_range['min']
    print(min_price)
    max_price = price_range['max']
    print(max_price)
    price_filtered = Product.objects.filter(id__in=product_list, price__in=(min_price, max_price))
    print(price_filtered)
    return price_filtered


def filtered_list(request):
    result = request.POST
    filtered_by_attrs = []
    filter_dict = result.lists()
    filter_set = create_filterset(filter_dict)

    if filter_set['attribute_filter'] == {}:
        url = request.META['HTTP_REFERER']
        category = int(url.split('/')[4])
        products = AttributeValue.objects.filter(product_id__category__id=category, product_id__is_active=True)

    else:
        products = recurs_filter(filter_set=filter_set['attribute_filter'])

    for item in products.values('product_id'):
        filtered_by_attrs.append(item['product_id'])
    price_filtered = price_filtered_products(filtered_by_attrs, filter_set['price_filter'])

    return {'product_list': price_filtered, 'attr_filters': filter_set['attribute_filter'],
            'price_filter': filter_set['price_filter']}


# ________________________________________________________________________


def category_products(request, category_id=None):
    if request.method == 'POST':
        filtered_products = filtered_list(request)
        filter_set = filtered_products['attr_filters']
        price_filters = filtered_products['price_filter']
        products_list = Product.objects.filter(id__in=filtered_products['product_list'], is_active=True)
    else:
        products_list = Product.objects.filter(is_active=True, category=category_id)
        price_filters = get_price_filter(products_list)
        filter_set = {}

    filter_values = get_category_attributes(category_id)
    content = {
        'title': ProductCategory.objects.get(id=category_id).name,
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': products_list,
        'price_filter': price_filters,
        'filters': filter_values,
        'filter_set': filter_set,
        'current_category': category_id,
    }
    return render(request, 'mainapp/products.html', content)


# def search_items(request):
#     data = request.GET['search']
#     items = Product.objects.filter(name__contains=data.title())
#     items = items | Product.objects.filter(name__contains=data.lower())
#     print(items)
#     return HttpResponse('success')
