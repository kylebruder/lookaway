from django import forms
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget
from .models import Image, Sound 

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
