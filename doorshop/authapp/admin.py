from django.contrib import admin

from authapp.models import ShopUser


@admin.register(ShopUser)
class AdminShopUser(admin.ModelAdmin):
    list_display = ("username", "is_active")
