# Generated by Django 4.1.7 on 2023-03-15 11:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MaxLengthValidator(12)]),
        ),
    ]
