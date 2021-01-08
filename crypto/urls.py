from django.urls import path
import crypto.views as views

app_name= "crypto"

urlpatterns = [
    # Read Views
    path(
        'wallets/bitcoin/',
        views.BitcoinWalletListView.as_view(),
        name='bitcoinwallets',
    ),
    path(
        'wallets/litecoin/',
        views.LitecoinWalletListView.as_view(),
        name='litecoinwallets',
    ),
    path(
        'wallets/bitcoin/<int:pk>/',
        views.BitcoinWalletDetailView.as_view(),
        name='bitcoinwallet_detail',
    ),
    path(
        'wallets/litecoin/<int:pk>/',
        views.LitecoinWalletDetailView.as_view(),
        name='litecoinwallet_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/donations/bitcoin/',
        views.MemberBitcoinWalletView.as_view(),
        name='member_bitcoinwallets',
    ),
    path(
        'member/<slug:member>/donations/litecoin/',
        views.MemberLitecoinWalletView.as_view(),
        name='member_litecoinwallets',
    ),
    # Create VIews
    path(
        'add/bitcoin-wallet/',
        views.BitcoinWalletCreateView.as_view(),
        name='bitcoinwallet_create',
    ),
    path(
        'add/litecoin-wallet/',
        views.LitecoinWalletCreateView.as_view(),
        name='litecoinwallet_create',
    ),
    # Update Views
    path(
        'modify/bitcoin-wallet/<int:pk>/',
        views.BitcoinWalletUpdateView.as_view(),
        name='bitcoinwallet_update',
    ),
    path(
        'modify/litecoin-wallet/<int:pk>/',
        views.LitecoinWalletUpdateView.as_view(),
        name='litecoinwallet_update',
    ),
    # Delete Views
    path(
        'delete/bitcoin-wallet/<int:pk>/',
        views.BitcoinWalletDeleteView.as_view(),
        name='bitcoinwallet_delete',
    ),
    path(
        'delete/litecoin-wallet/<int:pk>/',
        views.LitecoinWalletDeleteView.as_view(),
        name='litecoinwallet_delete',
    ),

]
