# Generated by Django 5.1.4 on 2024-12-10 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosperson',
            name='password_confirm',
            field=models.CharField(max_length=20, null=True, verbose_name='confirmar contraseña'),
        ),
    ]
