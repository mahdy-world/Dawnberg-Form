from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Status Name'))
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))

    def __str__(self):
        return self.name


class Form(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Form Title'))
    description = models.CharField(max_length=100, verbose_name=_('Form Description'))
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Created By'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Created At'))
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))

    def __str__(self):
        return self.title

    def visits_count(self):
        return self.instance_set.all().count()

    def answers_count(self):
        return self.instance_set.filter(is_submitted=True).count()


class Question(models.Model):
    question_type = (
        (1, 'نص قصير'),
        (2, 'نص طويل'),
        (3, 'اختيار متعدد '),
        (4, 'واحد من متعدد'),
        (5, 'رقم تليفون'),
        (5, 'بريد إلكتروني'),
    )
    form = models.ForeignKey(Form, verbose_name="المنوذج", on_delete=models.CASCADE)
    question_name = models.CharField(max_length=50, verbose_name=_('Question Title'))
    question_type = models.IntegerField(choices=question_type, verbose_name=_('Question Type'))
    required = models.BooleanField(default=False, verbose_name=_('Required'))
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))

    def __str__(self):
        return self.question_name


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, verbose_name=_('Question'), on_delete=models.CASCADE)
    option = models.CharField(max_length=50, verbose_name=_('Option'))
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))

    def __str__(self):
        return self.option


class Instance(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name=_('Form'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    assigned_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                          verbose_name=_('Assigned To'))
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Status'))
    is_submitted = models.BooleanField(default=False, verbose_name=_('Is Submitted?'))
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))

    def __str__(self):
        return str(self.form.title)

    def calls_count(self):
        return self.instancecall_set.all().count()


class Answer(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, verbose_name=_('Question'), on_delete=models.CASCADE)
    text_answer = models.TextField(verbose_name=_('Answer'), null=True, blank=True)
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ['question__id']


class InstanceComment(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True, verbose_name=_('Notes'))
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))


class InstanceCall(models.Model):
    call_status = (

        (1, _('Answered')),
        (2, _('Not Answered')),
        (3, _('Busy')),
        (4, _('Unreachable'))
    )


    call_type_choices = (
        (1, 'مكالمة صادرة'),
        (2, 'مكالمة واردة'),
        (3, 'Whatsapp'),
        (4, 'Messenger'),



        (5, 'E-Mail')

    )

    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Employee'))
    status = models.IntegerField(choices=call_status, verbose_name=_('Call Status'))
    call_type = models.IntegerField(choices=call_type_choices, verbose_name=_('Call Type'))
    summary = models.TextField(null=True, blank=True, verbose_name=_('Call Summary'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))
    deleted = models.BooleanField(default=False, verbose_name=_('Delete'))

    def __str__(self):
        return str(self.id)

    def call_type_icon(self):
        if self.call_type == 1:
            return 'fa fa-arrow-up'
        if self.call_type == 2:
            return 'fa fa-arrow-down'
        if self.call_type == 3:
            return 'fab fa-whatsapp'
        if self.call_type == 4:
            return 'fab fa-facebook-messenger'

    def call_type_badge(self):
        if self.call_type == 1:
            return 'badge badge-info'
        if self.call_type == 2:
            return 'badge badge-danger'
        if self.call_type == 3:
            return 'badge badge-success'
        if self.call_type == 4:
            return 'badge badge-primary'


class CallHistory(models.Model):
    call_type_choices = (
        (1, 'Add Call'),
        (2, 'Edit Call'),
        (3, 'Delete Call')
    )
    instance = models.ForeignKey(Instance, verbose_name="Answer", on_delete=models.CASCADE)
    call_type = models.IntegerField(choices=call_type_choices, verbose_name="نوع العملية")
    call_by = models.ForeignKey(User, verbose_name="Employee", on_delete=models.CASCADE, null=True, blank=True)
    call = models.ForeignKey(InstanceCall, verbose_name="Call", on_delete=models.CASCADE)
    add_at = models.DateTimeField(auto_now_add=True)
