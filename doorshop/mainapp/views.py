from django.forms import modelform_factory, modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from mainapp.forms import AttributeFormSet, AttributesForm
from mainapp.models import ProductCategory, Product, AttributeValue, ProductAttributes
from mainapp.serializers import product_list_serializer


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


def category_products(request, category_id=None):
    products_list = Product.objects.filter(is_active=True, category=category_id)
    filter_values = get_category_attributes(category_id)
    if len(products_list) > 1:
        min_price_product = products_list.order_by('price')[0],
        max_price_product = products_list.order_by('-price')[0],
        min = float(min_price_product[0].get_price())
        max = float(max_price_product[0].get_price())
        price_filter = {
            "min": int(round(min)),
            "max": int(round(max)),
        }
    else:
        price_filter = None
    content = {
        'title': ProductCategory.objects.get(id=category_id).name,
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': products_list,
        'price_filter': price_filter,
        'filters': filter_values,
    }

    return render(request, 'mainapp/products.html', content)


# filtered_products = FilteredProductList()

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
                buffer = AttributeValue(
                    attribite_id=attr_id,
                    product_id=item['product_id'],
                    value=val
                )
                result = result | buffer
        return result


def recurs_filter(filter_set, founded_products=None, counter=0):
    if counter == len(filter_set):
        founded_products = product_list_serializer(founded_products)
        return founded_products
    else:
        for key, values in filter_set:
            if founded_products:
                founded_products = simple_filter(attr_id=key, values=values, founded_products=founded_products)
                filter_set.pop(key)
                counter += 1
                recurs_filter(filter_set, founded_products, counter)
            else:
                founded_products = simple_filter(attr_id=key, values=values)
                filter_set.pop(key)
                counter += 1
                recurs_filter(filter_set, founded_products, counter)


@csrf_exempt
def filtered_list(request):
    if request.method == 'POST' and request.is_ajax():
        result = request.POST
        print(result)
        return HttpResponse('success')
    return HttpResponse('FAIL!!!!!')

# def clear_filters(request):
#     if request.is_ajax():
#         filtered_products.filter_set = {}
#         filtered_products.founded_items = Product.objects.none()
#     return JsonResponse(filtered_products.filter_set)
