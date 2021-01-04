from django.urls import path
import crypto.views as views

app_name= "crypto"

urlpatterns = [
    # Read Views
    path(
        'wallets/bitcoin/',
        views.BitcoinWalletListView.as_view(),
        name='bitcoin_wallets',
    ),
    path(
        'wallets/litecoin/',
        views.LitecoinWalletListView.as_view(),
        name='litecoin_wallets',
    ),
    path(
        'wallets/bitcoin/<int:pk>/',
        views.BitcoinWalletDetailView.as_view(),
        name='bitcoin_wallet_detail',
    ),
    path(
        'wallets/litecoin/<int:pk>/',
        views.LitecoinWalletDetailView.as_view(),
        name='litecoin_wallet_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/donations/bitcoin/',
        views.MemberBitcoinWalletView.as_view(),
        name='member_bitcoin_wallets',
    ),
    path(
        'member/<slug:member>/donations/litecoin/',
        views.MemberLitecoinWalletView.as_view(),
        name='member_litecoin_wallets',
    ),
    # Create VIews
    path(
        'add/bitcoin-wallet/',
        views.BitcoinWalletCreateView.as_view(),
        name='bitcoin_wallet_create',
    ),
    path(
        'add/litecoin-wallet/',
        views.LitecoinWalletCreateView.as_view(),
        name='litecoin_wallet_create',
    ),
    # Update Views
    path(
        'modify/bitcoin-wallet/<int:pk>/',
        views.BitcoinWalletUpdateView.as_view(),
        name='bitcoin_wallet_update',
    ),
    path(
        'modify/litecoin-wallet/<int:pk>/',
        views.LitecoinWalletUpdateView.as_view(),
        name='litecoin_wallet_update',
    ),
    # Delete Views
    path(
        'delete/bitcoin-wallet/<int:pk>/',
        views.BitcoinWalletDeleteView.as_view(),
        name='bitcoin_wallet_delete',
    ),
    path(
        'delete/litecoin-wallet/<int:pk>/',
        views.LitecoinWalletDeleteView.as_view(),
        name='litecoin_wallet_delete',
    ),

]
