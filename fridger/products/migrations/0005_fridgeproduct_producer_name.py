# Generated by Django 3.2.7 on 2021-12-15 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_fridgeproduct_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='fridgeproduct',
            name='producer_name',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
