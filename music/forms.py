from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image, Sound, Video, Code, Link
from .models import Album, Track

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

class AlbumForm(forms.ModelForm):

    cover = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="Choose an iconic image as the cover for the Album",
        label="Cover Image",
    )
    title = forms.CharField(
        help_text="""The Album title will appear on the site and is used to \
            create the permanent URL for the Album  
            It will also appear on search engine results pages (SERPs) and \
            can impact search engine optimization (SEO)
            The optimal format is 'Primary Keyword - Secondary Keyword | \
            Brand Name'""",
        max_length=128,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of the Album 
            The description will be used by Search Engines and will impact \
            SEO
            Include key words used in the title
            Keep it less than 155 characters""",
        max_length=155,
        required=False, 
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Provide some information and context about the Album",
        max_length=65535,
    )
    artist = forms.CharField(
        help_text="Which artist or artists performed the music on this Album?",
        max_length=128,
    )
    genre = forms.CharField(
        help_text="What kind of music is in this Album? (optional)",
        max_length=128,
        required=False, 
    )
    year = forms.DecimalField(
        help_text="Which year was this Album released? (optional)",
        max_digits=4,
        required=False, 
    )
    label = forms.CharField(
        help_text="Which label released this Album? (optional)",
        max_length=128,
        required=False, 
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    artist.widget.attrs.update({'class': 'form-text-field'})
    genre.widget.attrs.update({'class': 'form-text-field'})
    year.widget.attrs.update({'class': 'form-text-field'})
    label.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Album
        fields = (
            'title',
            'meta_description',
            'cover',
            'tracks',
            'text',
            'artist',
            'genre',
            'year',
            'label',
            'links',
            'tags',
        )
        help_texts = {
            'cover': """Choose an image to represent the Album cover
                For best results use an image with a 1:1 aspect ratio \
                (optional)""",
            'links': """Add one or more links related the this Album
                Example: label website/band website/purchase options \
                (optional)""",
            'tags': "Add one or more tags",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AlbumForm, self).__init__(*args, **kwargs)
        self.fields['tracks'].queryset = Track.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['cover'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class TrackForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        help_text="Choose an Image that represents the Track (optional)",
        required=False,
    )
    title = forms.CharField(
        help_text="""The Track title will appear on the site and is used to \
            create the permanent URL for the Track
            It will also appear on search engine results pages (SERPs) and can \
            impact search engine optimization (SEO)
            The optimal format is 'Primary Keyword - Secondary Keyword | Brand \
            Name'""",
        max_length=128,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of the Track
            The description will be used by Search Engines and will impact SEO
            Include key words used in the title
            Keep it less than 155 characters""",
        max_length=155,
        required=False,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Provide some information and context about the Track",
        max_length=65535,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the Track will appear in Track \
            lists on Albums
            Lower order values will appear first""",
        max_digits=8,
        initial=0,
    )
    artist = forms.CharField(
        help_text="Which artist or artists performed the music on this Track?",
        max_length=128,
    )
    genre = forms.CharField(
        help_text="What kind of music is this Track? (optional)",
        max_length=128,
        required=False,
    )
    year = forms.DecimalField(
        help_text="Which year was this Track released? (optional)",
        max_digits=4,
        required=False, 
    )
    label = forms.CharField(
        help_text="Which label released this Track? (optional)",
        max_length=128,
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    order.widget.attrs.update({'class': 'form-text-field'})
    artist.widget.attrs.update({'class': 'form-text-field'})
    genre.widget.attrs.update({'class': 'form-text-field'})
    year.widget.attrs.update({'class': 'form-text-field'})
    label.widget.attrs.update({'class': 'form-text-field'})


    class Meta:
        model = Track
        fields = (
            'sound',
            'title',
            'order',
            'meta_description',
            'image',
            'text',
            'artist',
            'genre',
            'year',
            'label',
            'video',
            'links',
            'tags',
        )
        help_texts = {
            'cover': """Choose an image to represent the Album cover
                For best results use an image with a 1:1 aspect ratio \
                (optional)""",
            'sound': "Select the Sound file for the Track",
            'video': "Add a music video for the Track (optional)",
            'links': """Add one or more links related the this Album
                Example: label website/band website/purchase options \
                (optional)""",
            'tags': "Add one or more tags (optional)",
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TrackForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['sound'].queryset = Sound.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['video'].queryset = Video.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
