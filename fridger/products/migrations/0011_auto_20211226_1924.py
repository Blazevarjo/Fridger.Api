# Generated by Django 3.2.7 on 2021-12-26 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_shoppinglistproduct_shopping_list_fragment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppinglistproduct',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AddField(
            model_name='shoppinglistproduct',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
