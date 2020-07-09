from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget
from members.models import Member
from .models import Image, Sound, Code, Link, Tag 

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


class ImageCreateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = [
            'title',
            'image_file',
            'text',
            'credit',
        ]
        widgets = {
            'image_file': ImagePreviewWidget
        }
        help_texts = {
            'title': "Give the image a memorable and unique title that will be easy to reference later.",
            'image_file': "Obtain permission before uploading depicitons of private persons or places. Image Preview will appear when successfully uploaded.",
            'text': "The text may appear on pages that include Images or other objects that use Images",
            'credit': "Give credit to the original creator of the image file. Obtain expressed permission before uploading images with exclusive rights.",
        }

class ImageUpdateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = [
            'title',
            'text',
            'credit',
        ]
        help_texts = {
            'title': "Give the image a memorable and unique title that will be easy to reference later.",
            'text': "The text may appear on pages that include Images or other objects that use Images",
            'credit': "Give credit to the original creator of the image file. Obtain expressed permission before uploading images with exclusive rights.",
        }

class SoundCreateForm(forms.ModelForm):

    class Meta:
        model = Sound
        fields = [
            'title',
            'sound_file',
            'text',
            'credit',
        ]
        widgets = {
            'sound_file': SoundPreviewWidget
        }
        help_texts = {
            'title': "Give the sound a memorable and unique title that will be easy to reference later.",
            'sound_file': "Obtain permission before uploading depicitons of private persons or places. Sound Preview will appear when successfully uploaded.",
            'text': "The text may appear on pages that include Sounds or other objects that use Sounds",
            'credit': "Give credit to the original creator of the sound file. Obtain expressed permission before uploading sounds with exclusive rights.",
        }

class SoundUpdateForm(forms.ModelForm):

    class Meta:
        model = Sound
        fields = [
            'title',
            'text',
            'credit',
        ]
        help_texts = {
            'title': "Give the sound a memorable and unique title that will be easy to reference later.",
            'text': "The text may appear on pages that include Sounds or other objects that use Sounds",
            'credit': "Give credit to the original creator of the sound file. Obtain expressed permission before uploading sounds with exclusive rights.",
        }

class CodeForm(forms.ModelForm):

    class Meta:
        model = Code
        fields = [
            'title',
            'code',
            'language',
            'language_version',
            'file_path',
            'source',
        ]
        widgets = {
            'code': Textarea(attrs={
                'wrap': 'off',
                'class': 'code-box',
            }),
        }
        help_texts = {
            'title': "Give the code sample a memorable and unique title that will be easy to reference later.",
            'code': "Enter the code here.",
            'language': "For which language is the code written?",
            'language_version': "For which version or versions of the language is the code written?",
            'file_path': "In which file does this code belong?",
            'source': "From where does the code originate? Please credit yourself or your source.",
        }

class LinkForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False,
        help_text=Link._meta.get_field('image').help_text,
    )

    class Meta:
        model = Link
        fields = [
            'title',
            'url',
            'image',
            'text',
        ]
        widgets = {
            'image': ImagePreviewWidget
        }
        help_texts = {
            'title': "Give the link a memorable and unique title that will be easy to reference later.",
            'image': "Choose an image that represents the linked resource. It is recommended to use an image close to a 1:1 aspect ratio because the image may be cropped when displayed on a page.",
            'url': "Enter the URL here.",
            'text': "The text may appear on pages that include Links or other objects that use Links",
        }

    def __init__(self, *args, **kwargs):
        member = Member.objects.get(pk=kwargs.pop('user').pk)
        super(LinkForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=member,
        ).order_by(
            '-creation_date',
        )

