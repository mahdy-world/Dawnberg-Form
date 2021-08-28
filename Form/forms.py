from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.models import inlineformset_factory
from .models import *


class MainForm(forms.ModelForm):
    class Meta:
        model = Form
        exclude = ['created_by']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'projectname', 'placeholder': 'Enter Form Title...',
                       'style': 'border: none; border-bottom: 2px solid #556ee6'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'projectdesc', 'placeholder': 'Enter Form Discraption...',
                       'style': 'border: none; border-bottom: 2px solid #556ee6'}),

            'deleted': forms.HiddenInput(),

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
        widgets = {
            'deleted': forms.HiddenInput(),
            'question_type': forms.HiddenInput(),
        }


class OptionsForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = ['option']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


OptionsFormSet = inlineformset_factory(Question, QuestionOption,
                                       form=OptionsForm, extra=10)


class CallForm(forms.ModelForm):
    instance_status = forms.ModelChoiceField(queryset=Status.objects.filter(deleted=False), required=False)

    class Meta:
        model = InstanceCall
        fields = ['call_type', 'status', 'summary', 'deleted']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = InstanceComment
        fields = ['comment', 'deleted']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


class ConvertForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ['assigned_employee', 'deleted']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


class InstanceDeleteForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ['deleted']
        widgets = {
            'deleted': forms.HiddenInput(),
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'
        widgets = {
            'deleted': forms.HiddenInput(),
        }


class ChangeInstanceStatusForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = ['status']
