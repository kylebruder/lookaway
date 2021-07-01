# Generated by Django 3.1.7 on 2021-03-31 16:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0006_auto_20210109_2203'),
        ('objects', '0014_auto_20201115_1955'),
        ('members', '0015_auto_20201228_2048'),
        ('art', '0003_auto_20201213_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='bitcoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.bitcoinwallet'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='litecoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.litecoinwallet'),
        ),
        migrations.AddField(
            model_name='visual',
            name='bitcoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.bitcoinwallet'),
        ),
        migrations.AddField(
            model_name='visual',
            name='litecoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.litecoinwallet'),
        ),
        migrations.CreateModel(
            name='ArtPageSection',
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
                ('code', models.ManyToManyField(blank=True, to='objects.Code')),
                ('galleries', models.ManyToManyField(blank=True, to='art.Gallery')),
                ('images', models.ManyToManyField(blank=True, to='objects.Image')),
                ('links', models.ManyToManyField(blank=True, to='objects.Link')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.member')),
                ('sounds', models.ManyToManyField(blank=True, to='objects.Sound')),
                ('tags', models.ManyToManyField(blank=True, to='objects.Tag')),
                ('videos', models.ManyToManyField(blank=True, to='objects.Video')),
                ('visuals', models.ManyToManyField(blank=True, to='art.Visual')),
            ],
            options={
                'verbose_name': 'Landing Page Section',
                'verbose_name_plural': 'Landing Page Sections',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ArtAppProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Lookaway CMS', max_length=255)),
                ('show_title', models.BooleanField(default=True)),
                ('meta_description', models.TextField(blank=True, max_length=155, null=True)),
                ('show_desc', models.BooleanField(default=True)),
                ('text', models.TextField(blank=True, max_length=65535, null=True)),
                ('n_visuals', models.PositiveIntegerField(default=25)),
                ('n_galleries', models.PositiveIntegerField(default=5)),
                ('visual_list_pagination', models.PositiveIntegerField(default=25)),
                ('gallery_list_pagination', models.PositiveIntegerField(default=6)),
                ('show_new_visuals', models.BooleanField(default=True)),
                ('show_top_visuals', models.BooleanField(default=True)),
                ('show_new_galleries', models.BooleanField(default=True)),
                ('show_top_galleries', models.BooleanField(default=True)),
                ('banner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_banner', to='objects.image')),
                ('bg_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_bg_image', to='objects.image')),
                ('bitcoin_wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.bitcoinwallet')),
                ('links', models.ManyToManyField(blank=True, to='objects.Link')),
                ('litecoin_wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.litecoinwallet')),
                ('logo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_logo', to='objects.image')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
