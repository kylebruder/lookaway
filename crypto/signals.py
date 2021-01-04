import re
import logging
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from pathlib import Path
from lookaway.settings import BASE_DIR
from .models import BitcoinWallet, LitecoinWallet, member_crypto_dir
from objects.utils import FileSystemOps

logger = logging.getLogger(__name__)

# Bitcoin Wallet35yy
@receiver(pre_save, sender=BitcoinWallet)
def make_bitcoin_qr(sender, instance, *args, **kwargs):
    '''
    Generates and saves usable Bitcoin wallet QR codes as WEBP images 
    to used with the wallet model.
    '''
    # Remove existing QR code image if one exists
    if instance.qr_code_lg:
        fsop = FileSystemOps()
        fsop._delete_file(instance.qr_code_lg.path)
    file_name = instance.public_address + "_btc.webp"
    img = instance.make_lg_qr(address=instance.public_address)
    p = Path('media')
    relative_path = member_crypto_dir(instance, file_name)
    qr_path = BASE_DIR / p / relative_path
    absolute_dir = qr_path.parents[1]
    absolute_dir.mkdir(parents=True, exist_ok=True)
    img.save(qr_path, "webp") 
    instance.qr_code_lg = str(relative_path)

@receiver(post_delete, sender=BitcoinWallet)
def remove_bitcoin_qr(sender, instance, *args, **kwargs):
    '''
    Remove QR code image files related to the deleted wallet instance from the filesystem
    '''
    fsop = FileSystemOps()
    if instance.qr_code_lg:
        fsop._delete_file(instance.qr_code_lg.path)

# Litecoin Wallet35yy
@receiver(pre_save, sender=LitecoinWallet)
def make_litecoin_qr(sender, instance, *args, **kwargs):
    '''
    Generates and saves usable Litecoin wallet QR codes as WEBP images
    to used with the wallet model.
    '''
    # Remove existing QR code image if one exists
    if instance.qr_code_lg:
        fsop = FileSystemOps()
        fsop._delete_file(instance.qr_code_lg.path)
    file_name = instance.public_address + "_ltc.jpg"
    img = instance.make_lg_qr(address=instance.public_address)
    p = Path('media')
    relative_path = member_crypto_dir(instance, file_name)
    qr_path = BASE_DIR / p / relative_path
    Path.mkdir(qr_path, parents=True, exist_ok=True)
    img.save(qr_path, "webp")
    instance.qr_code_lg = str(relative_path)

@receiver(post_delete, sender=LitecoinWallet)
def remove_litecoin_qr(sender, instance, *args, **kwargs):
    '''
    Remove QR code image files related to the deleted wallet instance from the filesystem
    '''
    fsop = FileSystemOps()
    if instance.qr_code_lg:
        fsop._delete_file(instance.qr_code_lg.path)
