from django.urls import path

from . import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.product, name='index'),
    # path('<int:id>/', mainapp.product, name='product'),
]