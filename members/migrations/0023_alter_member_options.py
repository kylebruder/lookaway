# Generated by Django 3.2 on 2021-04-26 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0022_rename_show_top_visual_profile_show_top_visuals'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['is_staff', 'is_superuser', '-date_joined']},
        ),
    ]
