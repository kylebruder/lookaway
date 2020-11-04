from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image, Sound, Video, Code, Link
from .models import Gallery, Visual

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

class GalleryForm(forms.ModelForm):

    visuals = CustomModelMultipleChoiceField(
        queryset=Image.objects.all(),
        help_text="""Choose which Visuals you would like to include \
            in the Gallery""",
    )
    title = forms.CharField(
        help_text="""The Gallery title will appear on the site and is used to \
            create the permanent URL for the Gallery
            It will also appear on search engine results pages (SERPs) and can \
            impact search engine optimization (SEO)
            The optimal format is 'Primary Keyword - Secondary Keyword | Brand \
            Name'""",
        max_length=128,
    )
    artist = forms.CharField(
        help_text="""Which artist or artists produced the Visuals included in \
            the Gallery?""",
        max_length=128,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of the Gallery
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
        help_text="""Provide some information and context about the Gallery \
            (optional)""",
        max_length=65535,
        required=False
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    artist.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Gallery
        fields = (
            'title',
            'visuals',
            'artist',
            'video',
            'meta_description',
            'text',
            'links',
            'tags',
        )
        help_texts = {
            'video': "Add a Video for the Gallery (optional)",
            'links': """Add one or more links related the the Gallery
                Example: art collective website/gallery website/purchase options \
                (optional)""",
            'tags': "Add one or more tags (optional)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(GalleryForm, self).__init__(*args, **kwargs)
        self.fields['visuals'].queryset = Visual.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-creation_date',
        )

class VisualForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""The Visual title will appear on the site and is used to \
            create the permanent URL for the Visual
            It will also appear on search engine results pages (SERPs) and can \
            impact search engine optimization (SEO)
            The optimal format is 'Primary Keyword - Secondary Keyword | Brand \
            Name'""",
        max_length=128,
    )
    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        help_text="Choose an Image for the Visual",
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the Visual will appear in \
            Galleries
            Lower order values will appear first""",
        max_digits=8,
        initial=0,
    )
    artist = forms.CharField(
        help_text="""Which artist or artists produced the Visual?""",
        max_length=128,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of the Visual
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
        help_text="""Provide some information and context about the Visual \
            (optional)""",
        max_length=65535,
        required=False
    )
    medium = forms.CharField(
        help_text="""What materials where used to produce the Visual?
            Example: Oil on Canvas, 35mm film, India ink on paper (optional)""",
        max_length=1028,
        required=False
    )
    credits = forms.CharField(
        help_text="""List any additional people that contributed to the \
            production of the Visual (optional)""",
        max_length=1028,
        required=False
    )
    year = forms.DecimalField(
        help_text="Which year was work on this Visual completed? (optional)",
        max_digits=4,
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    order.widget.attrs.update({'class': 'form-text-field'})
    artist.widget.attrs.update({'class': 'form-text-field'})
    medium.widget.attrs.update({'class': 'form-text-field'})
    credits.widget.attrs.update({'class': 'form-text-field'})
    year.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Visual
        fields = (
            'image',
            'video',
            'title',
            'order',
            'artist',
            'meta_description',
            'text',
            'medium',
            'credits',
            'year',
            'links',
            'tags',
        )
        help_texts = {
            'video': "Add a video (optional)",
            'links': """Add one or more links related the this Visual
                Example: label website/band website/purchase options \
                (optional)""",
            'tags': "Add one or more tags (optional)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(VisualForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
