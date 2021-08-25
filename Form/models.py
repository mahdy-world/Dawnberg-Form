from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=128)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.name


class Form(models.Model):
    title = models.CharField(max_length=50, )
    description = models.CharField(max_length=100, )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='انشئت بواسطة')
    created_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ الانشاء ')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.title


class Question(models.Model):
    question_type = (
        (1, 'نص قصير'),
        (2, 'نص طويل'),
        (3, 'اختيار متعدد '),
        (4, 'واحد من متعدد'),
        (5, 'رقم تليفون'),
    )
    form = models.ForeignKey(Form, verbose_name="المنوذج", on_delete=models.CASCADE)
    question_name = models.CharField(max_length=50, verbose_name='عنوان السؤال')
    question_type = models.IntegerField(choices=question_type)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.question_name


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, verbose_name="السؤال", on_delete=models.CASCADE)
    option = models.CharField(max_length=50, verbose_name='الاختيار')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.option


class Instance(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return str(self.form.title)

    def calls_count(self):
        return self.instancecall_set.all().count()


class Answer(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, verbose_name='السؤال', on_delete=models.CASCADE)
    text_answer = models.TextField(verbose_name='الإجابة', null=True, blank=True)
    optional_answer = models.TextField(verbose_name=' (اختيار من متعدد)الإجابة', null=True, blank=True)
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return str(self.question)

    class Meta:
        ordering = ['question__id']


class InstanceComment(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, verbose_name='حذف')


class InstanceCall(models.Model):
    call_status = (
        (1, 'تم الرد'),
        (2, 'لم يتم الرد'),
        (3, 'مشغول'),
        (4, 'مغلق أو غير متاح')
    )
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=call_status)
    summary = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False, )

    def __str__(self):
        return str(self.id)
