# Generated by Django 5.1.6 on 2025-02-12 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_category_recipes_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipes',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.category'),
        ),
    ]
