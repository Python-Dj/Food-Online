# Generated by Django 4.1.7 on 2023-03-16 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
