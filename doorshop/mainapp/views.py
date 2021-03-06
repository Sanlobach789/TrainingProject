from django.shortcuts import render

from mainapp.models import ProductCategory, Product


def main(request):

    content = {
        'title': 'Door-Shop'
    }
    return render(request, 'mainapp/index.html', content)


def products(request):

    content = {
        'title': 'GeekShop - Категории',
        'categories': ProductCategory.objects.filter(is_active=True),
        'products': Product.objects.filter(is_active=True),
    }
    return render(request, 'mainapp/products.html', content)
