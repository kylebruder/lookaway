# Generated by Django 3.0.7 on 2020-07-22 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(default='test'),
            preserve_default=False,
        ),
    ]
