# Generated by Django 3.0.7 on 2020-07-27 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_profile_media_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='media_capacity',
            field=models.PositiveIntegerField(default=500000000),
        ),
    ]
