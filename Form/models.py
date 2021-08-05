from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Form(models.Model):
    title = models.CharField(max_length=50,verbose_name="عنوان النموذج")
    description = models.TextField(verbose_name="تفاصيل النموذج")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE , verbose_name = 'انشئت بواسطة')
    created_at = models.DateTimeField(auto_now=True,  verbose_name='تاريخ الانشاء ')
    deleted = models.BooleanField(default=False, verbose_name='حذف')

    def __str__(self):
        return self.title


class Question(models.Model):
    qtype = (
        ('نص قصير','نص قصير'),
        ('نص طويل','نص طويل'),
        ('اختيار متعدد','اختيار متعدد '),
        ('واحد من متعدد ','واحد من متعدد')
    )
    form = models.ForeignKey(Form,verbose_name="المنوذج", on_delete=models.CASCADE) 
    question_name= models.CharField(max_length=50,verbose_name='عنوان السؤال')
    question_type=models.CharField(max_length=50, choices=qtype)  
    
    def __str__(self):
        return self.form