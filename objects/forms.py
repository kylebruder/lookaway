from django import forms
from templates.widgets import ImagePreviewWidget
from .models import Image 

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
            'text': "Captions may appear on pages that include Images or other objects that use Images",
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
            'text': "Captions may appear on pages that include Images or other objects that use Images",
            'credit': "Give credit to the original creator of the image file. Obtain expressed permission before uploading images with exclusive rights.",
        }

