# Generated by Django 3.0.7 on 2020-08-24 22:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20200823_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitelink',
            name='expiration_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
