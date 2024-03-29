# Generated by Django 3.1.7 on 2021-03-29 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0017_auto_20210324_2238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterModelOptions(
            name='articlesection',
            options={'ordering': ['order'], 'verbose_name': 'Article Section', 'verbose_name_plural': 'Article Sections'},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name': 'Story', 'verbose_name_plural': 'Stories'},
        ),
        migrations.AlterModelOptions(
            name='storysection',
            options={'ordering': ['order'], 'verbose_name': 'Story Section', 'verbose_name_plural': 'Story Sections'},
        ),
        migrations.AlterModelOptions(
            name='supportdocsection',
            options={'ordering': ['order'], 'verbose_name': 'Information Section', 'verbose_name_plural': 'Information Sections'},
        ),
        migrations.AlterModelOptions(
            name='supportdocument',
            options={'verbose_name': 'Information', 'verbose_name_plural': 'Information'},
        ),
        migrations.AddField(
            model_name='documentationappprofile',
            name='show_desc',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='documentationappprofile',
            name='show_title',
            field=models.BooleanField(default=True),
        ),
    ]
