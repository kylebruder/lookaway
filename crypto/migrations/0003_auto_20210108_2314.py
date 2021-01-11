# Generated by Django 3.0.7 on 2021-01-08 23:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0002_auto_20201228_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitcoinwallet',
            name='public_address',
            field=models.CharField(default=uuid.uuid4, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='litecoinwallet',
            name='public_address',
            field=models.CharField(default=uuid.uuid4, max_length=64, null=True),
        ),
    ]