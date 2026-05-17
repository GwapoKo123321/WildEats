from django.urls import path
from .views import (
    add_new_order,
    add_order_item,
    delete_order,
    delete_order_item,
    order_summary,
    record_payment,
    reject_payment,
    sales_home,
    update_order_status,
    verify_payment,
)

urlpatterns = [
    path('', sales_home, name='sales_home'),
    path('addNewOrder/', add_new_order, name='add_new_order'),
    path('addOrderItem/<int:order_id>/', add_order_item, name='add_order_item'),
    path('deleteOrderItem/<int:order_id>/<int:item_id>/', delete_order_item, name='delete_order_item'),
    path('recordPayment/<int:order_id>/', record_payment, name='record_payment'),
    path('orderSummary/<int:order_id>/', order_summary, name='order_summary'),
    path('verifyPayment/<int:order_id>/<int:payment_id>/', verify_payment, name='verify_payment'),
    path('rejectPayment/<int:order_id>/<int:payment_id>/', reject_payment, name='reject_payment'),
    path('updateOrderStatus/<int:order_id>/', update_order_status, name='update_order_status'),
    path('deleteOrder/<int:order_id>/', delete_order, name='delete_order'),
]

