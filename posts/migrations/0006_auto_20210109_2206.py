# Generated by Django 3.0.7 on 2021-01-09 22:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20210109_2203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='BitcoinWallet',
            new_name='bitcoin_wallet',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='LitecoinWallet',
            new_name='litecoin_wallet',
        ),
    ]
