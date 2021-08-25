from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.models import inlineformset_factory
from .models import *


class MainForm(forms.ModelForm):
    class Meta:
        model = Form
        exclude = ['deleted', 'created_by']
        widgets = {

            'title': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'projectname', 'placeholder': 'Enter Form Title...',
                       'style': 'border: none; border-bottom: 2px solid #556ee6'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'projectdesc', 'placeholder': 'Enter Form Discraption...',
                       'style': 'border: none; border-bottom: 2px solid #556ee6'})
        }

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
        
#         widgets = {

                

#             'text_answer': forms.TextInput(
#                 attrs={'class': 'form-control', 'id': 'projectname', 'placeholder': 'Enter Form Title...',
#                        'style': 'border: none; border-bottom: 2px solid #556ee6'}),
#             'optional_answer': forms.TextInput(
#                 attrs={'class': 'form-control', 'id': 'projectdesc', 'placeholder': 'Enter Form Discraption...',
#                        'style': 'border: none; border-bottom: 2px solid #556ee6'})
#         }


        

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['form']


class OptionsForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = ['option']


OptionsFormSet = inlineformset_factory(Question, QuestionOption,
                                       form=OptionsForm, extra=10)


class CallForm(forms.ModelForm):
    class Meta:
        model = InstanceCall
        fields = ['status' , 'summary','employee' ,'deleted' ]

class CommentForm(forms .ModelForm):

    class Meta:
        model = InstanceComment
        fields = ['comment' , 'deleted']

class ConvertForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ['assigned_employee' ,'deleted']
    