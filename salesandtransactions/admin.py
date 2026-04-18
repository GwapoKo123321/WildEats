from django.contrib import admin
from .models import Order, OrderItem, PaymentRecord

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentRecord)
