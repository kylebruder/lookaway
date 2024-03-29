# Generated by Django 3.1.7 on 2021-04-14 01:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0014_auto_20201115_1955'),
        ('members', '0019_auto_20210413_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembersPageSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_public', models.BooleanField(default=False)),
                ('publication_date', models.DateTimeField(blank=True, null=True)),
                ('order', models.DecimalField(decimal_places=4, max_digits=8)),
                ('hide_title', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(blank=True, max_length=65535, null=True)),
                ('info', models.TextField(blank=True, max_length=65535, null=True)),
                ('alert', models.TextField(blank=True, max_length=65535, null=True)),
                ('is_enabled', models.BooleanField(default=False)),
                ('members_only', models.BooleanField(default=False)),
                ('code', models.ManyToManyField(blank=True, to='objects.Code')),
                ('images', models.ManyToManyField(blank=True, to='objects.Image')),
                ('links', models.ManyToManyField(blank=True, to='objects.Link')),
                ('members', models.ManyToManyField(blank=True, related_name='section_members', to='members.Member')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member')),
                ('sounds', models.ManyToManyField(blank=True, to='objects.Sound')),
                ('tags', models.ManyToManyField(blank=True, to='objects.Tag')),
                ('videos', models.ManyToManyField(blank=True, to='objects.Video')),
            ],
            options={
                'verbose_name': 'Landing Page Section',
                'verbose_name_plural': 'Landing Page Sections',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='MembersAppProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Lookaway CMS', max_length=255)),
                ('show_title', models.BooleanField(default=True)),
                ('meta_description', models.TextField(blank=True, max_length=155, null=True)),
                ('show_desc', models.BooleanField(default=True)),
                ('text', models.TextField(blank=True, max_length=65535, null=True)),
                ('show_members', models.BooleanField(default=True)),
                ('show_contributors', models.BooleanField(default=True)),
                ('n_members_models', models.PositiveIntegerField(default=25)),
                ('n_contributor_models', models.PositiveIntegerField(default=25)),
                ('members_list_pagination', models.PositiveIntegerField(default=25)),
                ('contributors_list_pagination', models.PositiveIntegerField(default=1000)),
                ('member_agreement', models.TextField(blank=True, max_length=65535, null=True)),
                ('banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members_banner', to='objects.image')),
                ('bg_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members_bg_image', to='objects.image')),
                ('links', models.ManyToManyField(blank=True, to='objects.Link')),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members_logo', to='objects.image')),
            ],
            options={
                'verbose_name': 'App Profile',
            },
        ),
    ]
