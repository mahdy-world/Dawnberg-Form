# Generated by Django 3.2.5 on 2021-08-15 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Branch', '0002_branch_created_by'),
        ('Employee', '0003_employee_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Branch.branch', verbose_name='الفرع'),
        ),
        migrations.DeleteModel(
            name='Branch',
        ),
    ]