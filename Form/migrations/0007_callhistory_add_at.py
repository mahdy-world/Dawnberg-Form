# Generated by Django 3.2.5 on 2021-08-26 19:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Form', '0006_callhistory_call_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='callhistory',
            name='add_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
