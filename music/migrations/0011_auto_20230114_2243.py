# Generated by Django 3.2.15 on 2023-01-14 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_alter_musicpagesection_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicappprofile',
            name='album_list_pagination',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='musicappprofile',
            name='title',
            field=models.CharField(default='Music', max_length=255),
        ),
        migrations.AlterField(
            model_name='musicappprofile',
            name='track_list_pagination',
            field=models.PositiveIntegerField(default=10),
        ),
    ]