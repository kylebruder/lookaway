# Generated by Django 3.0.7 on 2021-01-09 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0006_auto_20210109_2203'),
        ('posts', '0004_auto_20200928_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='BitcoinWallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.BitcoinWallet'),
        ),
        migrations.AddField(
            model_name='post',
            name='LitecoinWallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.LitecoinWallet'),
        ),
    ]
