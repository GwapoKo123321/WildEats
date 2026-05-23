from django import forms
from django.contrib.auth.models import User
from .models import Cafeteria, Report, Order

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1.5px solid #f0e0a0; padding: 12px; width: 100%; border-radius: 8px;'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1.5px solid #f0e0a0; padding: 12px; width: 100%; border-radius: 8px;'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'style': 'border: 1.5px solid #f0e0a0; padding: 12px; width: 100%; border-radius: 8px;'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'border: 1.5px solid #f0e0a0; padding: 12px; width: 100%; border-radius: 8px;'}),
        }

class CafeteriaForm(forms.ModelForm):
    class Meta:
        model = Cafeteria
        fields = ['name', 'location', 'operating_hours', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., WildEats Main'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CIT Building A'}),
            'operating_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 08:00-17:00'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'report_summary']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'report_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_cost', 'status']
        widgets = {
            'total_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g., 150.00'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }