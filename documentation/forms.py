from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget, FictionWidget
from crypto.models import BitcoinWallet, LitecoinWallet
from members.models import Member
from objects.models import Image, Sound, Video, Code, Link
from .models import Article, ArticleSection, Story, StorySection, SupportDocument, SupportDocSection

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

class ArticleForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="Choose an image that represents the Article",
    )
    title = forms.CharField(
        help_text="""The Article title will appear on the site and is used to \
            create the permanent URL for the Article
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
        help_text="""Add a short description of the Article
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
        help_text="""Introduce the topic and context of the Article""",
        label="Introduction",
        max_length=65535,
        required=False,
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
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    class Meta:
        model = Article
        fields = (
            'title',
            'meta_description',
            'intro',
            'outro',
            'image',
            'links',
            'tags',
            'bitcoin_wallet',
            'litecoin_wallet',
        )
        help_texts = {
            'image': """Choose an image that represents the topic of the \
                Article (optional)""",
            'links': "Add one or more links (optional)",
            'tags': "Add one or more tags (optional)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['bitcoin_wallet'].queryset = BitcoinWallet.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['litecoin_wallet'].queryset = LitecoinWallet.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class ArticleSectionForm(forms.ModelForm):

    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="""Choose one or more images to include in this Section \
        (optional)""",
    )
    title = forms.CharField(
        help_text="""The Section title will appear as the heading of the \
            Section in the Article""",
        max_length=255,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Enter the Article Section text here",
        max_length=65535,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the Section will appear in the \
            Articleation
            Lower values will appear first""",
        max_digits=8,
        initial=0,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = ArticleSection
        fields = (
            'article',
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
            'article': """Choose the Article in which this Section \
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
        # Populate Article field
        if 'article' in kwargs:
            article = kwargs.pop('article')
            kwargs.update(initial={
                'article': article
            })
        super(ArticleSectionForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Article.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['images'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['sounds'].queryset = Sound.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['videos'].queryset = Video.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['code'].queryset = Code.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class SupportDocumentForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="Choose an image that represents the Support Document",
    )
    title = forms.CharField(
        help_text="""The title will appear on the site and is used to \
            create the permanent URL for the Support Document page
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
            The meta description is used by Search Engines
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
        required=False,
    )
    outro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Restate the key points in your Information and anything \
            supporting the validity and source.""",
        label="Conclusion",
        max_length=65535,
        required=False,
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
            'bitcoin_wallet',
            'litecoin_wallet',
        )
        help_texts = {
            'image': """Choose an image that represents the topic of the \
                Support Document (optional)""",
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
            '-last_modified',
        )
        self.fields['bitcoin_wallet'].queryset = BitcoinWallet.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['litecoin_wallet'].queryset = LitecoinWallet.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class SupportDocSectionForm(forms.ModelForm):

    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more Images to include in this Section",
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
        help_text="Enter the Section text here",
        max_length=65535,
        required=False,
    )
    tip = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Provide a useful tip that will be helpful for this Section",
        max_length=65535,
        required=False,
    )
    warning = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Warn your readers of any pitfalls related to this Section",
        max_length=65535,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the Section will appear in the \
            Support Document
            Lower values will appear first""",
        max_digits=8,
        initial=0,
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
            'tip',
            'warning',
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
                Information (optional)""",
            'sounds': """Choose one or more Sounds that support your \
                Information (optional)""",
            'videos': """Choose one or more Videos that support your \
                Information (optional)""",
            'code': """Choose one or more Code samples that support your \
                Information (optional)""",
            'links': """Choose one or more Links that provide reference to your \
                Information (optional)""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        # Populate Article field
        if 'support_document' in kwargs:
            support_document = kwargs.pop('support_document')
            kwargs.update(initial={
                'support_document': support_document
            })
        super(SupportDocSectionForm, self).__init__(*args, **kwargs)
        self.fields['support_document'].queryset = SupportDocument.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['images'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['sounds'].queryset = Sound.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['videos'].queryset = Video.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['code'].queryset = Code.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class StoryForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False,
        help_text="Choose an image that represents the Story",
    )
    title = forms.CharField(
        help_text="""The Story title will appear on the site and is used to \
            create the permanent URL for the Story. \
            It will also appear on search engine results pages (SERPs) and can \
            impact search engine optimization (SEO). \
            The optimal format is 'Primary Keyword - Secondary Keyword | Brand \
            Name'.""",
        max_length=128,
    )
    author = forms.CharField(
        help_text="""Who originally told or wrote this story?""",
        max_length=128,
    )
    is_fiction = forms.BooleanField(
        widget=FictionWidget(),
        help_text=  "Is this a true story or a work of fiction?",
        label="Non-Fiction/Fiction",
        required=False,
    )    
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of the Story. \
            The description will be used by Search Engines and will impact SEO. \
            Include key words used in the title.\
            Keep it less than 155 characters.""",
        max_length=155,
        label="Meta Description",
    )
    editor = forms.CharField(
        help_text="""Who edited this story?""",
        max_length=128,
        label="Editor(s) (optional)",
        required=False,
    )
    translator = forms.CharField(
        help_text="""Who translated this story?""",
        max_length=128,
        label="Translator(s) (optional)",
        required=False,
    )
    intro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Introduce the topic and context of the Story""",
        label="Foreword (optional)",
        max_length=65535,
        required=False,
    )
    outro = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Restate any information, observations, evidence or other \
            details and tie it all together""",
        label="Afterword (optional)",
        max_length=65535,
        required=False,
    )
    original_publisher = forms.CharField(
        help_text="""Who originally published this story?""",
        max_length=128,
        label="Orignal Publisher (optional)",
        required=False,
    )
    original_publication_year = forms.DecimalField(
        help_text="Which year was this Story originally published? (optional)",
        max_digits=4,
        label="Original Year of Publication (optional)",
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    author.widget.attrs.update({'class': 'form-text-field'})
    editor.widget.attrs.update({'class': 'form-text-field'})
    translator.widget.attrs.update({'class': 'form-text-field'})
    original_publisher.widget.attrs.update({'class': 'form-text-field'})
    original_publication_year.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Story
        fields = (
            'title',
            'author',
            'is_fiction',
            'meta_description',
            'translator',
            'editor',
            'original_publisher',
            'original_publication_year',
            'intro',
            'outro',
            'image',
            'links',
            'tags',
            'bitcoin_wallet',
            'litecoin_wallet',
        )
        help_texts = {
            'image': """Choose an image that represents the topic of the \
                Story (optional)""",
            'links': "Add one or more links (optional)",
            'tags': "Add one or more tags (optional)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(StoryForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['bitcoin_wallet'].queryset = BitcoinWallet.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['litecoin_wallet'].queryset = LitecoinWallet.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class StorySectionForm(forms.ModelForm):

    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="""Choose one or more images to include in this Section \
        (optional)""",
    )
    title = forms.CharField(
        help_text="""The Section title will appear as the heading of the \
            Section in the Story""",
        max_length=255,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Enter the Section text here",
        max_length=65535,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the Section will appear in the \
            Story
            Lower values will appear first""",
        max_digits=8,
        initial=0,
    )
    hide_title = forms.BooleanField(
        help_text =  """Choose this option if you do not want \
            the title of this section to be displayed on the Story page""",
        required=False,
    )    
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = StorySection
        fields = (
            'story',
            'title',
            'hide_title',
            'order',
            'text',
            'images',
        )
        help_texts = {
            'story': """Choose the Story in which this Section \
                will appear""",
            'hide_title': """Choose this option if you do not want \
                the title of this section to be displayed on the Story page""",
            'images': """Choose one or more Images that complement \
                this section of the story (optional)""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        # Populate Story field
        if 'story' in kwargs:
            story = kwargs.pop('story')
            kwargs.update(initial={
                'story': story
            })
        super(StorySectionForm, self).__init__(*args, **kwargs)
        self.fields['story'].queryset = Story.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['images'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
