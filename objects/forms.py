from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from .models import Image, Sound, Video, Code, Link, Tag 

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
            'tags',
        ]
        widgets = {
            'image_file': ImagePreviewWidget
        }
        help_texts = {
            'title': "Give the image a memorable and unique title that will be easy to reference later.",
            'image_file': "Obtain permission before uploading depicitons of private persons or places. Image Preview will appear when successfully uploaded.",
            'text': "The text may appear on pages that include Images or other objects that use Images",
            'credit': "Give credit to the original creator of the image file. Obtain expressed permission before uploading images with exclusive rights.",
            'tags': "Choose one or more tags that relate to the Image.",
        }

class ImageUpdateForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = [
            'title',
            'text',
            'credit',
            'tags',
        ]
        help_texts = {
            'title': "Give the image a memorable and unique title that will be easy to reference later.",
            'text': "The text may appear on pages that include Images or other objects that use Images",
            'credit': "Give credit to the original creator of the image file. Obtain expressed permission before uploading images with exclusive rights.",
            'tags': "Choose one or more tags that relate to the Image.",
        }

class SoundCreateForm(forms.ModelForm):

    class Meta:
        model = Sound
        fields = [
            'title',
            'sound_file',
            'text',
            'credit',
            'tags',
        ]
        widgets = {
            'sound_file': SoundPreviewWidget
        }
        help_texts = {
            'title': "Give the sound a memorable and unique title that will be easy to reference later.",
            'sound_file': "Obtain permission before uploading depicitons of private persons or places. Sound Preview will appear when successfully uploaded.",
            'text': "The text may appear on pages that include Sounds or other objects that use Sounds",
            'credit': "Give credit to the original creator of the sound file. Obtain expressed permission before uploading sounds with exclusive rights.",
            'tags': "Choose one or more tags that relate to the Sound.",
        }

class SoundUpdateForm(forms.ModelForm):

    class Meta:
        model = Sound
        fields = [
            'title',
            'text',
            'credit',
            'tags',
        ]
        help_texts = {
            'title': "Give the sound a memorable and unique title that will be easy to reference later.",
            'text': "The text may appear on pages that include Sounds or other objects that use Sounds",
            'credit': "Give credit to the original creator of the sound file. Obtain expressed permission before uploading sounds with exclusive rights.",
            'tags': "Choose one or more tags that relate to the Sound.",
        }

class VideoCreateForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = [
            'title',
            'video_file',
            'text',
            'credit',
            'tags',
        ]
        widgets = {
            'video_file': VideoPreviewWidget
        }

        help_texts = {
            'title': "Give the video a memorable and unique title that will be easy to reference later.",
            'video_file': "Obtain permission before uploading depicitons of private persons or places. Video Preview will appear when successfully uploaded.",
            'text': "The text may appear on pages that include Videos or other objects that use Videos",
            'credit': "Give credit to the original creator of the video file. Obtain expressed permission before uploading videos with exclusive rights.",
            'tags': "Choose one or more tags that relate to the Video.",
        }

class VideoUpdateForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = [
            'title',
            'text',
            'credit',
            'tags',
        ]
        help_texts = {
            'title': "Give the video a memorable and unique title that will be easy to reference later.",
            'text': "The text may appear on pages that include Videos or other objects that use Videos",
            'credit': "Give credit to the original creator of the video file. Obtain expressed permission before uploading videos with exclusive rights.",
            'tags': "Choose one or more tags that relate to the Video.",
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
            'source_url',
            'tags',
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
            'source_url': "Does the source have a website or webpage? If so enter it here.",
            'tags': "Choose one or more tags that relate to the Code.",
        }

class LinkForm(forms.ModelForm):

    class Meta:
        model = Link
        fields = [
            'title',
            'url',
            'text',
            'favicon_href',
            'tags',
        ]
        help_texts = {
            'title': "Give the tag a memorable and unique title that will be easy to reference later.",
            'url': "Enter the URL here.",
            'text': "The text may appear on pages that include Links or other objects that use Links.",
            'favicon_href': "Enter a URL for the webpage image.",
            'tags': "Choose one or more tags that relate to the Link.",
        }

class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = [
            'key',
            'value',
        ]
        help_texts = {
            'key': "Enter a word or words that describe a category",
            'value': "Enter words or numbers that describe a qualative or quantative value",
        }
