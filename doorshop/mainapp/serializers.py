from django.http import JsonResponse

from mainapp.models import Product


def product_list_serializer(product_queryset):
    product_list = Product.objects.none()
    for product_id in product_queryset.values('product_id'):
        product_list = product_list | Product.objects.filter(id=product_id['product_id'])
    result_products = {}
    for product in product_list.values():
        result_products[product['id']] = {'id': product['id'],
                                          'product_name': product['name'],
                                          'product_price': product['price'],
                                          'image': product['image']}
    return JsonResponse({'result': result_products})
