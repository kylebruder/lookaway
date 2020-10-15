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

    title = forms.CharField(
        help_text="""Give the Image a memorable and unique title that will be \
            easy to reference later""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""The Image text may appear on pages that include Images""",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the image file\
            Obtain expressed permission before uploading images with exclusive \
            rights""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Image
        fields = [
            'image_file',
            'title',
            'text',
            'credit',
            'tags',
        ]
        widgets = {
            'image_file': ImagePreviewWidget
        }
        help_texts = {
            'title': """Give the image a memorable and unique title that will \
                be easy to reference later""",
            'image_file': """Obtain permission before uploading depicitons of \
                private persons or places
                Image Preview will appear when successfully uploaded""",
            'text': """The text may appear on pages that include Images or \
                other objects that use Images""",
            'credit': """Give credit to the original creator of the image file
                Obtain expressed permission before uploading images with \
                exclusive rights""",
            'tags': "Choose one or more tags",
        }

class ImageUpdateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Image a memorable and unique title that will be \
            easy to reference later""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""The Image text may appear on pages that include Images""",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        max_length=256,
        help_text="""Give credit to the original creator of the image file\
            Obtain expressed permission before uploading images with exclusive \
            rights""",
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Image
        fields = [
            'title',
            'text',
            'credit',
            'tags',
        ]
        help_texts = {
            'tags': "Choose one or more tags",
        }

class SoundCreateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Sound a memorable and unique title that will be \
            easy to reference later""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Images",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Sound file
            Obtain expressed permission before uploading sounds with exclusive \
            rights""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})
    class Meta:
        model = Sound
        fields = [
            'sound_file',
            'title',
            'text',
            'credit',
            'tags',
        ]
        widgets = {
            'sound_file': SoundPreviewWidget
        }
        help_texts = {
            'sound_file': """Obtain permission before uploading depicitons of \
                private persons or places
                Sound Preview will appear when successfully uploaded""",
            'tags': "Choose one or more tags",
        }

class SoundUpdateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Sound a memorable and unique title that will be \
            easy to reference later""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Images",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Sound file
            Obtain expressed permission before uploading sounds with exclusive \
            rights""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Sound
        fields = [
            'title',
            'text',
            'credit',
            'tags',
        ]
        help_texts = {
            'tags': "Choose one or more tags",
        }

class VideoCreateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Video memorable and unique title that will be easy \
            to reference later""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Images",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Video file
            Obtain expressed permission before uploading videos with exclusive \
            rights.""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Video
        fields = [
            'video_file',
            'title',
            'text',
            'credit',
            'tags',
        ]
        widgets = {
            'video_file': VideoPreviewWidget
        }

        help_texts = {
            'video_file': """Obtain permission before uploading depicitons of \
                private persons or places
                Video Preview will appear when successfully uploaded""",
            'tags': "Choose one or more tags",
        }

class VideoUpdateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Video memorable and unique title that will be easy \
            to reference later""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Videos",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Video file
            Obtain expressed permission before uploading videos with exclusive \
            rights.""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})


    class Meta:
        model = Video
        fields = [
            'title',
            'text',
            'credit',
            'tags',
        ]
        help_texts = {
            'tags': "Choose one or more tags",
        }


class CodeForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Code sample a memorable and unique title that will \
            be easy to reference later""",
        max_length=256,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Include comments with your Code (optional)",
        label="Comments",
        max_length=65535,
        required=False,
    )
    code = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'wrap': 'off',
                'class': 'code-box',
            }
        ),
        help_text="Enter the code here",
        max_length=1024,
    )
    language= forms.CharField(
        help_text="For which language is the code written?",
        max_length=64,
    )
    language_version= forms.CharField(
        help_text="""For which version or versions of the language is the code \
            written?""",
        max_length=64,
    )
    file_path = forms.CharField(
        help_text="In which file does this code belong? (optional)",
        max_length=256,
        required=False,
    )
    source = forms.CharField(
        help_text="""From where does the code originate?
            Please credit yourself or your source (optional)""",
        max_length=64,
        required=False,
    )
    source_url = forms.CharField(
        help_text="""Does the source have a website or webpage?
            If so enter it here (optional)""",
        max_length=256,
        required=False,
    )

    language.widget.attrs.update({'class': 'form-text-field'})
    language_version.widget.attrs.update({'class': 'form-text-field'})
    file_path.widget.attrs.update({'class': 'form-text-field'})
    source.widget.attrs.update({'class': 'form-text-field'})
    source_url.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Code
        fields = [
            'title',
            'code',
            'language',
            'language_version',
            'text',
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
            'tags': "Choose one or more tags",
        }

class LinkCreateForm(forms.ModelForm):

    url = forms.CharField(
        help_text="Enter the URL here",
        max_length=256,
    )
    url.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Link
        fields = [
            'url',
        ]
  
class LinkForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Link a memorable and unique title that will be \
            easy to reference later""",
        max_length=256,
        required=False,
    )
    url = forms.CharField(
        help_text="Enter the URL here",
        max_length=256,
    )
    text = forms.CharField(
        help_text="The text may appear on pages that include Links",
        max_length=512,
        required=False,
    )
    favicon_href = forms.CharField(
        help_text="Enter a URL for the webpage image",
        max_length=256,
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    text.widget.attrs.update({'class': 'form-text-field'})
    url.widget.attrs.update({'class': 'form-text-field'})
    favicon_href.widget.attrs.update({'class': 'form-text-field'})

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
            'tags': "Choose one or more tags",
        }

class TagForm(forms.ModelForm):

    key = forms.CharField(
        help_text="Enter a word or words that describe a category",
        max_length=64,
    )
    value = forms.CharField(
        help_text="""Enter words or numbers that describe a qualitative or \
            quantitative value""",
        max_length=64,
        required=False,
    )
    key.widget.attrs.update({'class': 'form-text-field'})
    value.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Tag
        fields = [
            'key',
            'value',
        ]
