# Generated by Django 3.2.15 on 2023-01-14 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210506_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeappprofile',
            name='nav_objects_name',
            field=models.CharField(default='Multimedia', max_length=64),
        ),
        migrations.AlterField(
            model_name='homeappprofile',
            name='title',
            field=models.CharField(default='lookaway', max_length=255),
        ),
    ]
