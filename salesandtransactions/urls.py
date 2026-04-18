from django.urls import path
from .views import sales_home, add_new_order,add_order_item

urlpatterns = [
    path('', sales_home, name='sales_home'),
    path('addNewOrder/', add_new_order, name='add_new_order'),
    path('addOrderItem/<int:order_id>/', add_order_item, name='add_order_item'),
]

