# Generated by Django 5.0.6 on 2024-10-23 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_responsaveldependente_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='responsaveldependente',
            unique_together={('responsavel', 'dependente')},
        ),
    ]
