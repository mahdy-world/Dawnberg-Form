from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.models import inlineformset_factory
from .models import *

# <input type="text" class="form-control docs-date" name="date" placeholder="Pick a date" autocomplete="off">

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['deleted', 'created_by']
        widgets = {

            'start_date': forms.TextInput(
                attrs={'class': 'form-control docs-date' , 'type':'date' 
                       }),
            'end_date': forms.TextInput(
                attrs={'class': 'form-control docs-date' , 'type':'date'})
        }

class EmployeeDeleteForm(forms.ModelForm):
        class Meta:
            model = Employee
            fields = ['deleted']

# <input type="text" name="name" maxlength="128" class="form-control" placeholder="الاسم" title="" required="" id="id_name">

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        widgets = {
            'username':forms.TextInput(
                attrs={
                'class' :'form-control',
                
            }),
            
            'password': forms.PasswordInput(
                attrs={
                 'class' : 'form-control',

                'id':'id_password'
            })
        }


class RegisterFormEdit(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        widgets = {
            'username':forms.TextInput(
                attrs={
                'class' :'form-control',
                
            }),
            
            'password': forms.PasswordInput(
                attrs={
                 'class' : 'form-control',

                'id':'id_password'
            })
        }
