from django import forms
from django.contrib.admin.widgets import AdminDateWidget

from .models import *


class MainForm(forms.ModelForm):

    class Meta:
        model = Form
        exclude = ['deleted' ,'created_by']
        widgets = {

            'title' : forms.TextInput(attrs={'class':'form-control' , 'id':'projectname' ,'placeholder':'Enter Form Title...'}),
            'description':forms.Textarea(attrs={'class':'form-control' ,'id':'projectdesc',  'placeholder':'Enter Form Discraption...'})
        }
    