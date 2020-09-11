from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image
from .models import SupportDocument, Section

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

class SupportDocumentForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
    )
    title = forms.CharField(
        help_text="The Document title will appear on the site and is used to create the permanent URL for this Document. It will also appear on search engine results pages (SERPs) and can impact search engine optimization (SEO). The optimal format is 'Primary Keyword - Secondary Keyword | Brand Name'.",
        max_length=128,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Add a short description of this Document. The description will be used by Search Engines and will impact SEO. Include key words used in the title. Keep it less than 155 characters.",
        max_length=155,
        required=False, 
    )
    intro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Introduce the topic of the Support Document.",
        max_length=65535,
    )
    outro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Restate the concept of what is to be accomplished by following the Document.",
        max_length=65535,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    class Meta:
        model = SupportDocument
        fields = (
            'title',
            'meta_description',
            'intro',
            'outro',
            'image',
            'links',
            'numbered',
            'tags',
        )
        help_texts = {
            'image': "Choose an image that represents the topic of the Support Document.",
            'links': "Add one or more reference links.",
            'numbered': "Check this box if you would like the Sections of the Support Document to be displayed as a numbered list.",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SupportDocumentForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )

class SectionForm(forms.ModelForm):

    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
    )
    title = forms.CharField(
        help_text="Give the Section a memorable and unique title that will be easy to reference later.",
        max_length=255,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Enter your instructions here.",
        max_length=65535,
    )
    order = forms.DecimalField(
        help_text="Choose the order in which the Section will appear in the Support Document. Decimals are allowed.",
        max_digits=8,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Section
        fields = (
            'title',
            'support_document',
            'order',
            'text',
            'images',
            'sounds',
            'videos',
            'code',
            'links',
            'support_reference',
        )
        help_texts = {
            'support_document': "Choose the Support Document in which this Section will appear.",
            'support_reference': "Does this Section reference another Support Document? Add one here. (optional)",
            'images': "Choose one or more Images that support your instructions. (optional)",
            'sounds': "Choose one or more Sounds that support your instructions. (optional)",
            'videos': "Choose one or more Videos that support your instructions. (optional)",
            'code': "Choose one or more Code samples that support your instructions. (optional)",
            'links': "Choose one or more Links that provide reference to your instructions. (optional)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['images'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
