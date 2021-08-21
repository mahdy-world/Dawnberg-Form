# Generated by Django 3.2.5 on 2021-08-16 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0004_auto_20210815_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='', verbose_name='الملف')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.employee', verbose_name='الموظف')),
            ],
        ),
    ]