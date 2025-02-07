# Generated by Django 5.1.5 on 2025-02-07 02:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='saldo_atual',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
