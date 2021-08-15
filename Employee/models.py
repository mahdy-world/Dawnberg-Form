from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Branch(models.Model):
    name = models.CharField(max_length=128, verbose_name='الاسم')
    address = models.CharField(max_length=128, verbose_name='العنوان', null=True, blank=True)
    phone = models.CharField(max_length=128, verbose_name='التليفون', null=True, blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        default_permissions = ()
        permissions = (
            ('add_branch', 'إضافة فرع'),
            ('edit_branch', 'تعديل فرع'),
            ('delete_branch', 'حذف فرع'),
            ('access_branch_menu', 'الدخول علي قائمة الفروع'),
        )


class Employee(models.Model):

    employee_types = (
        (1, 'متقدم لوظيفة'),
        (2, 'موظف مؤقت'),
        (3, 'موظف دائم'),
    )

    religion_choices = (
        (1, 'مسلم'),
        (2, 'مسيحي'),
        (3, 'يهودي'),
    )
    social_state_choices = (
        (1, 'أعزب'),
        (2, 'خاطب'),
        (3, 'متزوج'),
        (4, 'مطلق'),
        (5, 'أرمل')
    )
    military_state_choices = (
        (1, 'معفي نهائي'),
        (2, 'معفي مؤقت'),
        (3, 'أتم فترة التجنيد'),
    )

    name = models.CharField(max_length=1024, verbose_name='الاسم بالكامل')
    image = models.ImageField(null = True , blank=True ,verbose_name="الصورةالشخصية")
    phone = models.CharField( max_length=14 , null=True , blank=True , verbose_name = "رقم الهاتف" )
    national_id = models.CharField(max_length=28, null=True, blank=True, verbose_name='رقم تحقيق الشخصية')
    branch = models.ForeignKey(Branch, verbose_name="الفرع", blank= True , null=True, on_delete=models.CASCADE)
    religion = models.IntegerField(choices=religion_choices, null=True, blank=True, verbose_name='الديانة')
    military_state = models.IntegerField(choices=military_state_choices, null=True, blank=True, verbose_name='موقف التجنيد')
    relationship = models.IntegerField(choices=social_state_choices, null=True, blank=True, verbose_name='الحالة الاجتماعية')
    salary = models.FloatField(null= True , blank=True , verbose_name = "الراتب")
    commition = models.FloatField(null= True, blank=True , verbose_name="العمولة")
    employe_contract = models.CharField(max_length=14, blank=True, null=True , verbose_name = "مدة عقد العمل")
    start_date = models.DateField(null=True, blank=True, verbose_name='تاريخ التعيين')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاريخ انتهاء العقد')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='حساب الموظف')
    employee_type = models.IntegerField(choices=employee_types, null=True, blank=True, verbose_name='نوع الموظف')
    created_by  = models.ForeignKey(User, on_delete=models.CASCADE , related_name="employee_created_by",verbose_name = "اضيف بواسطة")
    deleted = models.BooleanField(default=False, verbose_name='حذف')    

 
    def __str__(self):
        return self.name


# class EmployeeFile(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='الموظف')
#     file = models.FileField(verbose_name='الملف')

#     def __str__(self):
#         return self.file.name