from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from templates.widgets import ImagePreviewWidget
from .models import Member, Profile
from objects.models import Image

class CustomModelChoiceIterator(forms.models.ModelChoiceIterator):

    def choice(self, obj):
        return self.field.prepare_value(obj), self.field.label_from_instance(obj), obj

class CustomModelChoiceField(forms.models.ModelChoiceField):

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)

class CustomModelMultipleChoiceField(forms.models.ModelMultipleChoiceField):

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)

    choices = property(_get_choices, forms.MultipleChoiceField._set_choices)

class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(
        label="Member Login",
        max_length=32,
        help_text="""Use letters and numbers in your Member Login \
            Name. Your login name is used to create a permanent URL for \
            your Profile page. Your Member Login name is also used to credit \
            your contributions unless you choose a display name or provide \
            a first and last name.""",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Verify Password",
        )
    first_name = forms.CharField(
        widget=forms.PasswordInput(),
        label="First Name",
        help_text="""You may use your real name or an alias or completely fake \
            name. (optional)""",
    )
    last_name = forms.CharField(
        widget=forms.PasswordInput(),
        label="Last Name",
        help_text="""If you provide a first AND last name, they will be used  \
            to credit your contributions unless you have chosen a display \
            name. (optional)""",
    )
    email = forms.CharField(
        widget=forms.EmailInput(),
        label="Recovery Email",
        help_text="""If you provide an email contact, your email address will \
            only be used to recover your password in the event you no longer \
            know you password. (optional)""",
        required=False,
    )
    username.widget.attrs.update({'class': 'form-text-field'})
    password1.widget.attrs.update({'class': 'form-text-field'})
    password2.widget.attrs.update({'class': 'form-text-field'})
    first_name.widget.attrs.update({'class': 'form-text-field'})
    last_name.widget.attrs.update({'class': 'form-text-field'})
    email.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
        )

    # Thanks to Junior Mayta
    # https://stackoverflow.com/questions/52723824/how-to-create-a-validator-for-special-characters-in-django?rq=1
    def validate_username(self, string):
        '''
        Ensure the supplied username only contains lowercase letters and numbers
        Pass cleaned form data as a string
        returns either True or False
        '''
        for char in string:
            if not char.isdigit() and not char.isalpha():
                return False
        return True

    def clean_username(self):
        data = self.cleaned_data['username']
        if not data.islower():
            raise forms.ValidationError("Your username may only include lowercase letters.")
        if not self.validate_username(data):
            raise forms.ValidationError("Your username may only include letters and numbers.")
        return data
            
class MemberForm(forms.ModelForm):

    first_name = forms.CharField(
        required=False,
    )
    last_name = forms.CharField(
        required=False,
    )
    email = forms.CharField(
        required=False,
    )
    first_name.widget.attrs.update({'class': 'form-text-field'})
    last_name.widget.attrs.update({'class': 'form-text-field'})
    email.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Member
        fields = (
            'first_name',
            'last_name',
            'email',
        )

class ProfileForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        help_text="Choose your Profile Image. (optional)",
        required=False, 
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Explain yourself here.",
        required=False, 
    )
    class Meta:
        model = Profile
        fields = (
            'image',
            'text',
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
