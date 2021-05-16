from django.urls import path

from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products_index, name='index'),
    path('<int:category_id>/', mainapp.category_products, name='category_products'),
    path('detail/<int:product_id>/', mainapp.product_detail, name='product_detail'),
    # path('search/', mainapp.search_items, name='search_items'),
]
