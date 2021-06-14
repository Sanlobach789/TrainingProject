from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

import mainapp.context_processors
from mainapp.models import Product
from basketapp.models import Basket


@login_required
def basket_main(request):
    return render(request, 'basketapp/cart.html')


@login_required
def basket_add(request, id=None, qty=1):
    if request.is_ajax():
        product = get_object_or_404(Product, id=int(id))
        print(product)
        baskets = Basket.objects.filter(user=request.user, product=product)

        if not baskets.exists():
            basket = Basket(user=request.user, product=product)
            basket.quantity += int(qty)
            basket.save()

        else:
            basket = baskets.first()
            basket.quantity += int(qty)
            basket.save()

        result = {'total_quantity': basket.total_quantity(), 'in_stock': product.quantity}
        return JsonResponse({'result': result})


@login_required
def basket_add_ajax(request, id=None):
    if request.is_ajax():
        product = get_object_or_404(Product, id=int(id))
        baskets = Basket.objects.filter(user=request.user, product=product)
        product_remainder = product.get_remainder()

        if not baskets.exists():
            basket = Basket(user=request.user, product=product)
            basket.quantity += 1
            basket.save()
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()

        result = {'total_quantity': basket.total_quantity(), 'remainder': product_remainder}
        return JsonResponse({'result': result})


@login_required
def basket_remove(request, id=None):
    basket = Basket.objects.get(id=id)
    if basket.quantity > 1:
        basket.quantity -= 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket_item = Basket.objects.get(id=int(id))
        if quantity > 0:
            basket_item.quantity = quantity
            basket_item.save()
            result = {'quantity': basket_item.quantity, 'total_cost': basket_item.total_sum(),
                      'total_quantity': basket_item.total_quantity()}
        else:
            basket_item.delete()
            result = {'total_quantity': basket_item.total_quantity(), 'total_cost': basket_item.total_sum()}

        return JsonResponse({'result': result})
