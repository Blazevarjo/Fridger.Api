# Generated by Django 3.2.7 on 2021-12-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglistownership',
            name='ownership',
            field=models.CharField(choices=[('CREATOR', 'Creator'), ('ADMIN', 'Admin'), ('WRITE', 'Write'), ('READ', 'Read')], default='READ', max_length=7),
        ),
    ]
