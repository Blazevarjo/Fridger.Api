# Generated by Django 3.2.7 on 2021-12-20 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_shoppinglistproduct_shopping_list_fragment'),
        ('shopping_lists', '0006_alter_shoppinglist_fridge'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShoppingListFragment',
        ),
    ]
