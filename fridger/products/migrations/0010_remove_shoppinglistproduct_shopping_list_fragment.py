# Generated by Django 3.2.7 on 2021-12-20 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_qauntity_shoppinglistproduct_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppinglistproduct',
            name='shopping_list_fragment',
        ),
    ]
