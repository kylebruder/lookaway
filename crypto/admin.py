from django.contrib import admin
from .models import BitcoinWallet, LitecoinWallet

# Register your models here.

admin.site.register(BitcoinWallet)
admin.site.register(LitecoinWallet)
