# Generated by Django 3.2 on 2021-04-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20210422_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagesection',
            name='order',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
    ]
