from decimal import Decimal

from django import forms

from .models import MenuItem, Order, OrderItem, PaymentRecord


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


class MenuItemChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - \u20b1{obj.price:.2f}"


class OrderItemForm(forms.ModelForm):
    menu_item = MenuItemChoiceField(
        queryset=MenuItem.objects.none(),
        empty_label="Select a menu item",
        label="Menu Item",
    )

    def __init__(self, *args, vendor=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = MenuItem.objects.filter(is_available=True).select_related("vendor")
        if vendor is not None:
            queryset = queryset.filter(vendor=vendor)
        self.fields["menu_item"].queryset = queryset.order_by("name")
        self.fields["Quantity"].min_value = 1

    class Meta:
        model = OrderItem
        fields = ['menu_item', 'Quantity']


class MenuItemForm(forms.ModelForm):
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 3,
            "style": "min-height: 7rem; resize: vertical;",
        }),
    )
    price = PesoDecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.TextInput(attrs={
            'class': 'money-input',
            'placeholder': '\u20b10.00',
            'inputmode': 'decimal',
        })
    )

    class Meta:
        model = MenuItem
        fields = ["name", "description", "price", "is_available"]


class PaymentRecordForm(forms.ModelForm):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
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
        self.fields["PaymentMethod"].initial = "Cash"

    def clean_Amount(self):
        amount = self.cleaned_data['Amount']

        if self.order is None:
            return amount

        if amount != self.order.TotalCost:
            raise forms.ValidationError(
                f"Payment must cover the full order total of \u20b1{self.order.TotalCost:.2f}."
            )

        open_payment_total = sum(
            (
                payment.Amount
                for payment in self.order.payments.exclude(
                    PaymentStatus=PaymentRecord.STATUS_FAILED
                )
            ),
            Decimal("0.00"),
        )
        remaining_submittable = self.order.TotalCost - open_payment_total
        if amount > remaining_submittable:
            raise forms.ValidationError(
                f"Payment cannot exceed the remaining payable amount of \u20b1{remaining_submittable:.2f}."
            )

        return amount

    def clean_PaymentMethod(self):
        payment_method = self.cleaned_data["PaymentMethod"]
        if payment_method != "Cash":
            raise forms.ValidationError("Payments must be made in cash.")
        return payment_method

    class Meta:
        model = PaymentRecord
        fields = ['Amount', 'PaymentMethod']
