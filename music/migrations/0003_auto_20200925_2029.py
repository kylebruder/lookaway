# Generated by Django 3.1 on 2020-09-25 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_auto_20200924_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='title',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
