# Generated by Django 3.1.7 on 2021-04-13 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_profile_show_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberprofilesection',
            old_name='story',
            new_name='stories',
        ),
    ]