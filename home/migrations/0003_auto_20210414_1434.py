# Generated by Django 3.1.7 on 2021-04-14 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210413_1530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepagesection',
            old_name='story',
            new_name='stories',
        ),
    ]
