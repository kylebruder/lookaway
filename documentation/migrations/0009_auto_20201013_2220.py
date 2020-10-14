# Generated by Django 3.0.7 on 2020-10-13 22:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0013_auto_20200928_1714'),
        ('objects', '0012_auto_20200928_1714'),
        ('documentation', '0008_auto_20201013_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_public', models.BooleanField(default=False)),
                ('publication_date', models.DateTimeField(blank=True, null=True)),
                ('order', models.DecimalField(decimal_places=4, max_digits=8)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(blank=True, max_length=65535, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RenameModel(
            old_name='Document',
            new_name='Article',
        ),
        migrations.DeleteModel(
            name='DocumentSection',
        ),
        migrations.AddField(
            model_name='articlesection',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_article', to='documentation.Article'),
        ),
        migrations.AddField(
            model_name='articlesection',
            name='code',
            field=models.ManyToManyField(blank=True, to='objects.Code'),
        ),
        migrations.AddField(
            model_name='articlesection',
            name='images',
            field=models.ManyToManyField(blank=True, to='objects.Image'),
        ),
        migrations.AddField(
            model_name='articlesection',
            name='links',
            field=models.ManyToManyField(blank=True, to='objects.Link'),
        ),
        migrations.AddField(
            model_name='articlesection',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.Member'),
        ),
        migrations.AddField(
            model_name='articlesection',
            name='sounds',
            field=models.ManyToManyField(blank=True, to='objects.Sound'),
        ),
        migrations.AddField(
            model_name='articlesection',
            name='tags',
            field=models.ManyToManyField(blank=True, to='objects.Tag'),
        ),
        migrations.AddField(
            model_name='articlesection',
            name='videos',
            field=models.ManyToManyField(blank=True, to='objects.Video'),
        ),
    ]
