from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.models import inlineformset_factory
from .models import *


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['deleted', 'created_by']
        
        