# Generated by Django 5.0.6 on 2024-10-11 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_doacao_id_alter_projeto_foto_alter_projeto_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsavel',
            name='rm_dependente',
            field=models.ForeignKey(default=90136, on_delete=django.db.models.deletion.CASCADE, related_name='responsaveis', to='main.aluno'),
            preserve_default=False,
        ),
    ]
