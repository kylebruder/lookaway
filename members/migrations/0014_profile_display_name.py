# Generated by Django 3.0.7 on 2020-11-10 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_auto_20200928_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='display_name',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
