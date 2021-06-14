from django.urls import path, re_path

from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('<int:category_id>/', mainapp.products, name='products'),
    path('detail/<int:product_id>/', mainapp.product_detail, name='product_detail'),
    # path('search/', mainapp.search_items, name='search_items'),
]
