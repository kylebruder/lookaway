# Generated by Django 3.0.7 on 2020-06-29 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail_file',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='member_thumbnail_dir'),
        ),
    ]