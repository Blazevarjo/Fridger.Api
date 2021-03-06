# Generated by Django 3.2.7 on 2021-11-28 17:43


from django.db import migrations, models

import fridger.users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="friend",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
        migrations.AlterField(
            model_name="friend",
            name="is_accepted",
            field=models.BooleanField(default=False, verbose_name="Is friend request accepted"),
        ),
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(blank=True, upload_to=fridger.users.models.avatar_path, verbose_name="Avatar"),
        ),
        migrations.AlterField(
            model_name="user",
            name="can_use_real_name",
            field=models.BooleanField(default=False, verbose_name="Can display real name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True, verbose_name="Email"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=40,
                unique=True,
                verbose_name="Username",
            ),
            preserve_default=False,
        ),
    ]
