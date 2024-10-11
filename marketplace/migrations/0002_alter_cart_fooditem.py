# Generated by Django 4.1.7 on 2023-04-11 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_fooditem_category'),
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='fooditem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='menu.fooditem'),
        ),
    ]
