
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mainapp import views as mainapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp_views.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
