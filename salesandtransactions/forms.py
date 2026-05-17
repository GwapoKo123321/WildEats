from django import forms

from .models import Order, OrderItem, PaymentRecord


class PesoDecimalField(forms.DecimalField):
    def to_python(self, value):
        if isinstance(value, str):
            value = value.strip().replace(',', '')
            upper_value = value.upper()
            if upper_value.startswith('PHP'):
                value = value[3:].strip()
            elif value.startswith('\u20b1'):
                value = value[1:].strip()
            elif value.startswith('â‚±'):
                value = value[3:].strip()
            elif upper_value.startswith('P'):
                value = value[1:].strip()
        return super().to_python(value)

    def prepare_value(self, value):
        if value in (None, ''):
            return ''
        try:
            decimal_value = self.to_python(value)
        except forms.ValidationError:
            return value
        return f"\u20b1{decimal_value:.2f}"


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['CustomerName']


class OrderItemForm(forms.ModelForm):
    Price = PesoDecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={
            'class': 'money-input',
            'placeholder': '\u20b10.00',
            'inputmode': 'decimal',
        })
    )

    class Meta:
        model = OrderItem
        fields = ['ProductName', 'Quantity', 'Price']


class PaymentRecordForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('GCash', 'GCash'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    PaymentMethod = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)
    Amount = PesoDecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.TextInput(attrs={
            'class': 'money-input',
            'placeholder': '\u20b10.00',
            'inputmode': 'decimal',
        })
    )

    def __init__(self, *args, order=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order

    def clean_Amount(self):
        amount = self.cleaned_data['Amount']

        if self.order is None:
            return amount

        open_payment_total = sum(
            (
                payment.Amount
                for payment in self.order.payments.exclude(
                    PaymentStatus=PaymentRecord.STATUS_REJECTED
                )
            ),
            0,
        )
        remaining_submittable = self.order.TotalCost - open_payment_total
        if amount > remaining_submittable:
            raise forms.ValidationError(
                f"Payment cannot exceed the remaining payable amount of \u20b1{remaining_submittable:.2f}."
            )

        return amount

    class Meta:
        model = PaymentRecord
        fields = ['Amount', 'PaymentMethod']
