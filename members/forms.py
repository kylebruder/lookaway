from django import forms
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
