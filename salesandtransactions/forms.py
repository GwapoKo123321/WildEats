from django import forms
from .models import Order
from .models import OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['CustomerName']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['ProductName', 'Quantity', 'Price']