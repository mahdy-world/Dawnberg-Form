# Generated by Django 3.2.5 on 2021-08-14 01:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='الاسم')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='العنوان')),
                ('phone', models.CharField(blank=True, max_length=128, null=True, verbose_name='التليفون')),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
                'permissions': (('add_branch', 'إضافة فرع'), ('edit_branch', 'تعديل فرع'), ('delete_branch', 'حذف فرع'), ('access_branch_menu', 'الدخول علي قائمة الفروع')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024, verbose_name='الاسم بالكامل')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='الصورةالشخصية')),
                ('phone', models.CharField(blank=True, max_length=14, null=True, verbose_name='رقم الهاتف')),
                ('national_id', models.CharField(blank=True, max_length=28, null=True, verbose_name='رقم تحقيق الشخصية')),
                ('religion', models.IntegerField(blank=True, choices=[(1, 'مسلم'), (2, 'مسيحي'), (3, 'يهودي')], null=True, verbose_name='الديانة')),
                ('military_state', models.IntegerField(blank=True, choices=[(1, 'معفي نهائي'), (2, 'معفي مؤقت'), (3, 'أتم فترة التجنيد')], null=True, verbose_name='موقف التجنيد')),
                ('relationship', models.IntegerField(blank=True, choices=[(1, 'أعزب'), (2, 'خاطب'), (3, 'متزوج'), (4, 'مطلق'), (5, 'أرمل')], null=True, verbose_name='الحالة الاجتماعية')),
                ('salary', models.FloatField(blank=True, null=True, verbose_name='الراتب')),
                ('commition', models.FloatField(blank=True, null=True, verbose_name='العمولة')),
                ('employe_contract', models.CharField(blank=True, max_length=14, null=True, verbose_name='مدة عقد العمل')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='تاريخ التعيين')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='تاريخ انتهاء العقد')),
                ('employee_type', models.IntegerField(blank=True, choices=[(1, 'متقدم لوظيفة'), (2, 'موظف مؤقت'), (3, 'موظف دائم')], null=True, verbose_name='نوع الموظف')),
                ('deleted', models.BooleanField(default=False, verbose_name='حذف')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='حساب البرنامج')),
            ],
        ),
    ]
