# Generated by Django 3.1.7 on 2021-04-13 15:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0018_profile_show_email'),
        ('posts', '0014_postspagesection_members_only'),
        ('objects', '0014_auto_20201115_1955'),
        ('music', '0008_auto_20210412_1456'),
        ('art', '0005_artpagesection_members_only'),
        ('documentation', '0021_auto_20210409_1625'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeappprofile',
            name='nav_art_name',
            field=models.CharField(default='art', max_length=64),
        ),
        migrations.AlterField(
            model_name='homeappprofile',
            name='nav_documentation_name',
            field=models.CharField(default='zine', max_length=64),
        ),
        migrations.AlterField(
            model_name='homeappprofile',
            name='nav_music_name',
            field=models.CharField(default='music', max_length=64),
        ),
        migrations.AlterField(
            model_name='homeappprofile',
            name='nav_posts_name',
            field=models.CharField(default='posts', max_length=64),
        ),
        migrations.CreateModel(
            name='HomePageSection',
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
                ('albums', models.ManyToManyField(blank=True, to='music.Album')),
                ('articles', models.ManyToManyField(blank=True, to='documentation.Article')),
                ('code', models.ManyToManyField(blank=True, to='objects.Code')),
                ('documents', models.ManyToManyField(blank=True, to='documentation.SupportDocument')),
                ('galleries', models.ManyToManyField(blank=True, to='art.Gallery')),
                ('images', models.ManyToManyField(blank=True, to='objects.Image')),
                ('links', models.ManyToManyField(blank=True, to='objects.Link')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member')),
                ('posts', models.ManyToManyField(blank=True, to='posts.Post')),
                ('responses', models.ManyToManyField(blank=True, to='posts.ResponsePost')),
                ('sounds', models.ManyToManyField(blank=True, to='objects.Sound')),
                ('story', models.ManyToManyField(blank=True, to='documentation.Story')),
                ('tags', models.ManyToManyField(blank=True, to='objects.Tag')),
                ('tracks', models.ManyToManyField(blank=True, to='music.Track')),
                ('videos', models.ManyToManyField(blank=True, to='objects.Video')),
                ('visuals', models.ManyToManyField(blank=True, to='art.Visual')),
            ],
            options={
                'verbose_name': 'Home Page Section',
                'verbose_name_plural': 'Home Page Sections',
                'ordering': ['order'],
            },
        ),
    ]