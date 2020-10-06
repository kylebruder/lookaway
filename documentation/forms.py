from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image, Sound, Video, Code, Link
from .models import Document, DocumentSection, SupportDocument, SupportDocSection

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

class DocumentForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="Choose an image that represents the Document",
    )
    title = forms.CharField(
        help_text="""The Document title will appear on the site and is used to \
            create the permanent URL for the Document
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
        help_text="""Add a short description of the Document
            The description will be used by Search Engines and will impact SEO
            Include key words used in the title
            Keep it less than 155 characters""",
        max_length=155,
        required=False, 
    )
    intro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Introduce the topic and context of the information you \
            are sharing in this document""",
        label="Introduction",
        max_length=65535,
    )
    outro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Restate any information, observations, evidence or other \
            details and tie it all together""",
        label="Conclusion",
        max_length=65535,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    class Meta:
        model = Document
        fields = (
            'title',
            'meta_description',
            'intro',
            'outro',
            'image',
            'links',
            'tags',
        )
        help_texts = {
            'image': """Choose an image that represents the topic of the \
                Document (optional)""",
            'links': "Add one or more links (optional)",
            'tags': "Add one or more tags (optional)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )

class DocumentSectionForm(forms.ModelForm):

    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="""Choose one or more images that support your information \
        (optional)""",
    )
    title = forms.CharField(
        help_text="""The Section title will appear as the header of the \
            Section in the Document""",
        max_length=255,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Enter the Section information here",
        max_length=65535,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the Section will appear in the \
            Support Document
            Lower values will appear first""",
        max_digits=8,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = DocumentSection
        fields = (
            'document',
            'title',
            'order',
            'text',
            'images',
            'sounds',
            'videos',
            'code',
            'links',
        )
        help_texts = {
            'document': """Choose the Document in which this Section \
                will appear""",
            'images': """Choose one or more Images that support your \
                information (optional)""",
            'sounds': """Choose one or more Sounds that support your \
                information (optional)""",
            'videos': """Choose one or more Videos that support your \
                information (optional)""",
            'code': """Choose one or more Code samples that support your \
                information (optional)""",
            'links': """Choose one or more Links that provide reference to \
                your information (optional)""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(DocumentSectionForm, self).__init__(*args, **kwargs)
        self.fields['images'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
        self.fields['sounds'].queryset = Sound.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
        self.fields['videos'].queryset = Video.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
        self.fields['code'].queryset = Code.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )

class SupportDocumentForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="Choose an image that represents the Support Document",
    )
    title = forms.CharField(
        help_text="""The title will appear on the site and is used to \
            create the permanent URL for the Document page
            It will also appear on search engine results pages and \
            may impact search engine optimization
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
        help_text="""Add a short description of the Support Document
            The meta description is used by Search Engines and will impact SEO
            Include key words used in the title
            Keep it less than 155 characters""",
        max_length=155,
        required=False, 
    )
    intro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Introduce the topic of the Support Document",
        label="Introduciton",
        max_length=65535,
    )
    outro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Restate your direcitons and what has been accomplished by \
            following the Support Document""",
        label="Conclusion",
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
            'tags',
            'numbered',
        )
        help_texts = {
            'image': """Choose an image that represents the topic of the \
                Support Documenti (optional)""",
            'links': "Add one or more reference links (optional)",
            'tags': "Add one or more tags (optional)",
            'numbered': """Check this box if you would like the Sections of the \
            Support Document to be displayed as a numbered list""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SupportDocumentForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )

class SupportDocSectionForm(forms.ModelForm):

    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more Images to include in this Section",
    )
    title = forms.CharField(
        help_text="""The Section title will appear as the header of the \
            Section in the Support Document""",
        max_length=255,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Enter the Section instructions here",
        max_length=65535,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the Section will appear in the \
            Support Document
            Lower values will appear first""",
        max_digits=8,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = SupportDocSection
        fields = (
            'support_document',
            'title',
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
            'support_document': """Choose the Support Document in which this \
                Section will appear""",
            'support_reference': """Does this Section reference another Support \
                Document?
                Add one here (optional)""",
            'images': """Choose one or more Images that support your \
                instructions (optional)""",
            'sounds': """Choose one or more Sounds that support your \
                instructions (optional)""",
            'videos': """Choose one or more Videos that support your \
                instructions (optional)""",
            'code': """Choose one or more Code samples that support your \
                instructions (optional)""",
            'links': """Choose one or more Links that provide reference to your \
                instructions (optional)""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SupportDocSectionForm, self).__init__(*args, **kwargs)
        self.fields['images'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
        self.fields['sounds'].queryset = Sound.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
        self.fields['videos'].queryset = Video.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
        self.fields['code'].queryset = Code.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
