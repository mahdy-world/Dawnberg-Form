# Generated by Django 3.2.5 on 2021-08-15 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
    ]
