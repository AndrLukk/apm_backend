# Generated by Django 5.0.6 on 2024-10-23 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_responsaveldependente_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsaveldependente',
            name='dependente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependentes', to='main.aluno'),
        ),
    ]
