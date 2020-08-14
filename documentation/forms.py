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

    class Meta:
        model = SupportDocument
        fields = (
            'title',
            'intro',
            'outro',
            'image',
            'links',
            'numbered',
            'tags',
        )
        help_texts = {
            'title': "Give the Support Document a memorable and unique title that will be easy to reference later.",
            'intro': "Introduce the topic of the Support Document.",
            'outro': "Restate the concept of what is to be accomplished by following the Support Document.",
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
        )
        help_texts = {
            'title': "Give the Section a memorable and unique title that will be easy to reference later.",
            'support_document': "Choose the Support Document in which this Section will appear.",
            'order': "Choose the order in which the Section will appear in the Support Document. Decimals are allowed.",
            'text': "Enter the written instructions here.",
            'images': "Choose one or more Images that support your instructions.",
            'sounds': "Choose one or more Sounds that support your instructions.",
            'videos': "Choose one or more Videos that support your instructions.",
            'code': "Choose one or more Code samples that support your instructions.",
            'links': "Choose one or more Links that provide reference to your instructions.",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['images'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
