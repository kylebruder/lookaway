# Generated by Django 3.0.7 on 2020-11-17 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0010_auto_20201115_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='editor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='story',
            name='translator',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
