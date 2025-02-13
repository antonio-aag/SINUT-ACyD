# Generated by Django 5.0.6 on 2024-05-27 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Persona', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='personas',
            name='hijos',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personas',
            name='ape2',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='personas',
            name='telCasa',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='personas',
            name='telCelular',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
