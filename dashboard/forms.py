from django import forms
from .models import MonthlyFinance

class MonthlyFinanceForm(forms.ModelForm):
    class Meta:
        model = MonthlyFinance
        fields = ['savings_goal', 'debt']
        widgets = {
            'savings_goal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Savings Goal'}),
            'debt': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Debt Amount'}),
        }
