from django import forms
from .models import Customer
from datetime import date

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'amount']
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date', 'value': date.today()}),
        }
