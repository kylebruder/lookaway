# Generated by Django 3.0.7 on 2020-06-28 16:26

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_marshmallow_allocation', models.DateTimeField(default=django.utils.timezone.now)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Marshmallow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('weight', models.FloatField(default=0.0)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Member')),
            ],
        ),
    ]
