from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.models import inlineformset_factory
from .models import *


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        exclude = ['deleted', 'created_by']
        

class BranchDeleteForm(forms.ModelForm):
        class Meta:
            model = Branch
            fields = ['deleted']
