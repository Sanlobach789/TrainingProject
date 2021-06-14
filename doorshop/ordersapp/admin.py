from django.contrib import admin

from ordersapp.models import Order, OrderItem


admin.site.register(OrderItem)


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'created', 'updated', 'user',)
