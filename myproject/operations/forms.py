from django import forms
from .models import Cafeteria
from .models import Report

class CafeteriaForm(forms.ModelForm):
    class Meta:
        model = Cafeteria
        fields = ['name', 'location', 'operating_hours', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Cafeteria Name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'operating_hours': forms.TextInput(attrs={'placeholder': '00:00-00:00'}),
            'capacity': forms.NumberInput(attrs={'min': '1'}),
        }

class ReportForm(forms.ModelForm):
            class Meta:
                model = Report
                fields = ['report_type', 'report_summary']
                widgets = {
                    'report_type': forms.Select(attrs={'class': 'form-control'}),
                    'report_summary': forms.Textarea(
                        attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter report details...'}),
                }