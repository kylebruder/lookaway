import qrcode, hashlib, base58, binascii
import uuid
from sys import argv
from django.db import models
from objects.mixins import MetaDataMixin

# Create your models here.

def member_crypto_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/crypto/qr/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

class CryptoWallet(MetaDataMixin):
    '''
    Parent class for crypto currency wallets
    '''

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(
        max_length=1024,
        blank=True,
        null=True,
    )
    public_address = models.CharField(
        max_length=64,
        unique=True,
        default=uuid.uuid4
    )
    qr_code_lg = models.ImageField(
        upload_to=member_crypto_dir,
        max_length=255,
        blank=True,
        null=True,
    )

    def validate_public_address(self, address):
        '''
        Checks if a given sting is a valid Bitcoin or Litecoin public address.
        Returns True if the string is valid
        Thanks https://github.com/burakcanekici/BitcoinAddressValidator/blob/master/Main.py
        '''
        base58Decoder = base58.b58decode(address).hex()
        prefix_and_hash = base58Decoder[:len(base58Decoder)-8]
        checksum = base58Decoder[len(base58Decoder)-8:]
        h = prefix_and_hash
        for x in range(1,3):
            h = hashlib.sha256(binascii.unhexlify(h)).hexdigest()
        if checksum == h[:8]:
            return True
        else:
            return False

    def __str__(self):
        return self.title

class BitcoinWallet(CryptoWallet):

    def make_lg_qr(self, address):
        '''
        Given a valid Bitcoin address, returns a usable QR code image
        that contains the public address.
        '''
        return qrcode.make("bitcoin:" + str(address))

class LitecoinWallet(CryptoWallet):

    def make_lg_qr(self, address):
        '''
        Given a valid Litecoin address, returns a usable QR code image
        that contains the public address.
        '''
        return qrcode.make("litecoin:" + str(address))

    pass

class CryptoWalletsMixin(models.Model):

    class Meta:
        abstract = True

    bitcoin_wallet = models.ForeignKey(
        'crypto.BitcoinWallet',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    litecoin_wallet = models.ForeignKey(
        'crypto.LitecoinWallet',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
