# Generated by Django 5.1.1 on 2024-09-26 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_aluno_id_alter_aluno_rm'),
    ]

    operations = [
        migrations.AddField(
            model_name='projeto',
            name='titulo',
            field=models.CharField(default='teste', max_length=255),
            preserve_default=False,
        ),
    ]
