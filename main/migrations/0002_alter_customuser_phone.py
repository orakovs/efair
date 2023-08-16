# Generated by Django 4.2.4 on 2023-08-16 17:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message='Номер телефона должен быть в международном формате: +77011234567', regex='^\\+?1?\\d{12}$')]),
        ),
    ]
