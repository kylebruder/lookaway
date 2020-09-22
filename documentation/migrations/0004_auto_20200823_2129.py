# Generated by Django 3.0.7 on 2020-08-23 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0003_auto_20200803_2148'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='support_reference',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reference_doc', to='documentation.SupportDocument'),
        ),
        migrations.AddField(
            model_name='supportdocument',
            name='meta_description',
            field=models.TextField(blank=True, max_length=155, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='support_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_doc', to='documentation.SupportDocument'),
        ),
    ]