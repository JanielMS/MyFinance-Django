# Generated by Django 5.1.5 on 2025-01-31 07:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('saldo_atual', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('tipo', models.CharField(choices=[('Carteira', 'Carteira'), ('Poupança', 'Poupança'), ('Conta Corrente', 'Conta Corrente'), ('Investimentos', 'Investimentos'), ('VR/VA', 'VR/VA'), ('Outro', 'Outro')], max_length=15)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
