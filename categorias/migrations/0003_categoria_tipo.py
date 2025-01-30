# Generated by Django 5.1.2 on 2025-01-30 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categorias', '0002_categoria_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='tipo',
            field=models.CharField(choices=[('R', 'Receita'), ('D', 'Despesa')], default='D', max_length=1),
        ),
    ]
