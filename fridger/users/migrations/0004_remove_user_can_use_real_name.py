# Generated by Django 3.2.7 on 2022-01-12 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_mobile_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='can_use_real_name',
        ),
    ]
