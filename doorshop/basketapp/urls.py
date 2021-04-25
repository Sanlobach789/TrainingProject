import basketapp.views as basketapp
from django.urls import path

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket_main, name='basket_main'),
    path('add/<int:id>/<int:qty>/', basketapp.basket_add, name='basket_add'),
    path('add-to-cart/<int:id>/', basketapp.basket_add_ajax, name='basket_add_ajax'),
    path('remove/<int:id>/', basketapp.basket_remove, name='basket_remove'),
    path('edit/<int:id>/<int:quantity>/', basketapp.basket_edit, name='basket_edit'),
]