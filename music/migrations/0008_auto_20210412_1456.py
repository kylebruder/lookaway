# Generated by Django 3.1.7 on 2021-04-12 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0006_auto_20210109_2203'),
        ('music', '0007_musicpagesection_members_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='bitcoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.bitcoinwallet'),
        ),
        migrations.AddField(
            model_name='album',
            name='litecoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.litecoinwallet'),
        ),
        migrations.AddField(
            model_name='track',
            name='bitcoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.bitcoinwallet'),
        ),
        migrations.AddField(
            model_name='track',
            name='litecoin_wallet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crypto.litecoinwallet'),
        ),
    ]
