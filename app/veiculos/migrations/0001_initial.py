# Generated by Django 5.2 on 2025-05-26 23:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('obras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='veiculos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade_passageiros', models.PositiveIntegerField()),
                ('modelo', models.CharField(max_length=100)),
                ('cor', models.CharField(max_length=50)),
                ('placa', models.CharField(max_length=10, unique=True)),
                ('data_cadastro', models.DateField(auto_now_add=True)),
                ('obra_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='veiculos', to='obras.obras')),
            ],
            options={
                'db_table': 'veiculos',
            },
        ),
    ]
