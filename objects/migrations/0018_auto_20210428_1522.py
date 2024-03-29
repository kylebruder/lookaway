# Generated by Django 3.2 on 2021-04-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0017_auto_20210427_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectsappprofile',
            name='sound_crf',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='objectsappprofile',
            name='sound_qmax',
            field=models.PositiveIntegerField(default=51),
        ),
        migrations.AlterField(
            model_name='objectsappprofile',
            name='sound_qmin',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='objectsappprofile',
            name='video_crf',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='objectsappprofile',
            name='video_qmax',
            field=models.PositiveIntegerField(default=51),
        ),
        migrations.AlterField(
            model_name='objectsappprofile',
            name='video_qmin',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='objectspagesection',
            name='order',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
    ]
