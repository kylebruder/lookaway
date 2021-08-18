# Generated by Django 3.2 on 2021-05-07 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_alter_postspagesection_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-publication_date', '-creation_date'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='reportpost',
            options={'ordering': ['-publication_date', '-creation_date'], 'verbose_name': 'Report', 'verbose_name_plural': 'Reports'},
        ),
        migrations.AlterModelOptions(
            name='responsepost',
            options={'ordering': ['-publication_date', '-creation_date'], 'verbose_name': 'Response', 'verbose_name_plural': 'Responses'},
        ),
    ]