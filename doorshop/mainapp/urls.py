from django.urls import path

from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),
    path('<int:category_id>/', mainapp.category_products, name='category_products'),
    path('detail/<int:product_id>/', mainapp.product_detail, name='product_detail'),
    path('filters/', mainapp.filtered_list, name='filter_products'),
    # path('filters/<int:filter_id>/<str:filter_value>/<str:action>/', mainapp.filtered_list, name='filter_products'),
    # path('filters/clear/', mainapp.clear_filters, name='clear_filters'),
]
