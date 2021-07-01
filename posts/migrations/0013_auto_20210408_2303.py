# Generated by Django 3.1.7 on 2021-04-08 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0020_auto_20210331_1623'),
        ('posts', '0012_auto_20210407_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportpost',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='documentation.supportdocument'),
        ),
        migrations.AddField(
            model_name='responsepost',
            name='document',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='documentation.supportdocument'),
        ),
    ]
