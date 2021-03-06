from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from mainapp import views as mainapp_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('admin-staff/', include('adminapp.urls', namespace='admin_staff'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
