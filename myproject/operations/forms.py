from django import forms
from django.contrib.auth.models import User
from .models import Cafeteria, Report

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CafeteriaForm(forms.ModelForm):
    class Meta:
        model = Cafeteria
        fields = ['name', 'location', 'operating_hours', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Main Canteen'}),
            'location': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'e.g., 2nd Floor, Science Bldg'}),

            # This fixes the operating hours input field visual style and placeholder
            'operating_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 7:00 AM - 5:00 PM (or 07:00-17:00)'
            }),

            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'report_summary']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'report_summary': forms.Textarea(attrs={'placeholder': 'Summary details...', 'rows': 4}),
        }