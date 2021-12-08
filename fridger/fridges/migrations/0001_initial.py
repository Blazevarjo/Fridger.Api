# Generated by Django 3.2.7 on 2021-12-08 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FridgeOwnership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('permission', models.CharField(choices=[('ADMIN', 'Admin'), ('WRITE', 'Write'), ('READ', 'Read')], default='READ', max_length=5, verbose_name='User permission to fridger')),
                ('fridge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fridge_ownership', to='fridges.fridge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fridge_ownership', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
