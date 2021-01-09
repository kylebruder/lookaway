from django import forms
from django.contrib.auth.models import User
from .models import BitcoinWallet, LitecoinWallet

class BitcoinWalletForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Bitcoin Wallet a memorable and unique title that will be \
            easy to reference later""",
        max_length=256, 
        required=False,
    )
    public_address = forms.CharField(
        help_text="Enter the public address of your Bitcoin donation wallet here",
        max_length=256,
    )
    text = forms.CharField(
        help_text="Add a message describing what for what the proceeds from this address will be used",
        max_length=512,
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    public_address.widget.attrs.update({'class': 'form-text-field'})
    text.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = BitcoinWallet
        fields = [
            'title',
            'public_address',
            'text',
            'tags',
        ]

    def clean(self):
        cleaned_data = super().clean()
        error_msg = "Please Enter a valid Bitcoin Address"
        if BitcoinWallet.validate_public_address(self, cleaned_data.get('public_address')):
            pass
        else:
            self.add_error('public_address', error_msg)
            raise forms.ValidationError(error_msg, code=1)

class LitecoinWalletForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Litecoin Wallet a memorable and unique title that will be \
            easy to reference later""",
        max_length=256,
        required=False,
    )
    public_address = forms.CharField(
        help_text="Enter the public address of your Litecoin donation wallet here",
        max_length=256,
    )
    text = forms.CharField(
        help_text="Add a call to action describing what for what the proceeds from this address will be used",
        max_length=512,
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    public_address.widget.attrs.update({'class': 'form-text-field'})
    text.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = LitecoinWallet
        fields = [
            'title',
            'public_address',
            'text',
            'tags',
        ]

    def clean(self):
        cleaned_data = super().clean()
        error_msg = "Please Enter a valid Litecoin Address"
        if LitecoinWallet.validate_public_address(self, cleaned_data.get('public_address')):
            pass
        else:
            self.add_error('public_address', error_msg)
            raise forms.ValidationError(error_msg, code=1)

