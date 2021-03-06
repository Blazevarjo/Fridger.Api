# Generated by Django 3.2.7 on 2021-12-11 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping_lists', '0002_alter_shoppinglistownership_ownership'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingListFragment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameField(
            model_name='shoppinglistownership',
            old_name='ownership',
            new_name='permission',
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.DeleteModel(
            name='ShoppingListStatus',
        ),
    ]
