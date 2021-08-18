# Generated by Django 3.2 on 2021-04-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0022_auto_20210426_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlesection',
            name='order',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='documentationpagesection',
            name='order',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='storysection',
            name='order',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='supportdocsection',
            name='order',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
        ),
    ]