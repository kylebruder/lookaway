from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from art.models import Visual, Gallery
from documentation.models import Article, Story, SupportDocument
from music.models import Track, Album
from objects.models import Image, Sound, Video, Code, Link
from .models import HomeAppProfile, HomePageSection 

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

class HomeAppProfileForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""The title will appear in the header
            It will also appear on search engine results pages (SERPs) and can \
            impact search engine optimization (SEO)""",
        max_length=128,
        required=False,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of the website \
            The description will be used by Search Engines and will impact SEO \
            Include key words used on your page \
            Keep it less than 155 characters""",
        max_length=155,
        required=False,
    )
    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        help_text="Choose your Profile Image.",
        required=False, 
        label="Profile Image (optional)",
    )
    banner = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="""The banner is the background image for the home page \
            header
            The optimal image size is 1800 pixels wide by 400 pixels high \
            (9:2)""",
    )
    bg_image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        label="Background Image",
        help_text="The background image will appear on the home page \
            and lists of your contributions",
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Add a short blurb that will be displayed under the header",
        required=False, 
        label="Blurb (optional)",
    )

    class Meta:
        model = HomeAppProfile
        fields = (
            'image',
            'meta_description',
            'text',
            'banner',
            'bg_image',
        )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['banner'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['bg_image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class HomeAppProfileSettings(forms.ModelForm):
    show_new_posts = forms.BooleanField(
        label="Show the n newest posts on the home page",
        required=False,
    )
    show_top_posts = forms.BooleanField(
        label="Show the top n posts on the the home page",
        required=False,
    )
    show_new_responses = forms.BooleanField(
        label="Show the n newest responses on the home page",
        required=False,
    )
    show_top_responses = forms.BooleanField(
        label="Show the top n responses on the home page",
        required=False,
    )
    n_posts = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of posts to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_responses = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of responses to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_articles = forms.BooleanField(
        label="Show the n newest articles on the home page",
        required=False,
    )
    show_top_articles = forms.BooleanField(
        label="Show the top n articles on the home page",
        required=False,
    )
    show_new_stories = forms.BooleanField(
        label="Show the n newest stories on the home page",
        required=False,
    )
    show_top_stories = forms.BooleanField(
        label="Show the top n stories on the home page",
        required=False,
    )
    show_new_support_documents = forms.BooleanField(
        label="Show the n newest documents on the home page",
        required=False,
    )
    show_top_support_documents = forms.BooleanField(
        label="Show the top n documents on the home page",
        required=False,
    )
    n_articles = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of articles to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_stories = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of stories to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_documents = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of documents to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_visuals = forms.BooleanField(
        label="Show the n newest visuals on the home page",
        required=False,
    )
    show_top_visuals = forms.BooleanField(
        label="Show the top n visuals on the home page",
        required=False,
    )
    show_new_galleries = forms.BooleanField(
        label="Show the n newest galleries on the home page",
        required=False,
    )
    show_top_galleries = forms.BooleanField(
        label="Show the top n galleries on the home page",
        required=False,
    )
    n_visuals = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of visuals to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_galleries = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of galleries to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_tracks = forms.BooleanField(
        label="Show the n newest tracks on the home page",
        required=False,
    )
    show_top_tracks = forms.BooleanField(
        label="Show the top n tracks on the home page",
        required=False,
    )
    show_new_albums = forms.BooleanField(
        label="Show the n newest albums on the home page",
        required=False,
    )
    show_top_albums = forms.BooleanField(
        label="Show the top n albums on the home page",
        required=False,
    )
    n_tracks = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of tracks to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_albums = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of albums to show in each list on the home page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )

    class Meta:
        model = HomeAppProfile
        fields = (
            'show_new_posts',
            'show_top_posts',
            'show_new_responses',
            'show_top_responses',
            'n_posts',
            'n_responses',
            'show_new_articles',
            'show_top_articles',
            'show_new_stories',
            'show_top_stories',
            'show_new_documents',
            'show_top_documents',
            'n_articles',
            'n_stories',
            'n_documents',
            'show_new_visuals',
            'show_top_visuals',
            'show_new_galleries',
            'show_top_galleries',
            'n_visuals',
            'n_galleries',
            'show_new_tracks',
            'show_top_tracks',
            'show_new_albums',
            'show_top_albums',
            'n_tracks',
            'n_albums',
        )

class HomePageSectionForm(forms.ModelForm):

    is_enabled = forms.BooleanField(
        label="Enabled",
        help_text="""Choose this option if you want this section to appear\
            on the home page""",
        required=False,
    )
    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more Images to include in this Section",
    )
    title = forms.CharField(
        help_text="""The section title will appear in the header of this \
            section""",
        max_length=255,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Enter the section text here",
        max_length=65535,
        required=False,
    )
    info = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        label="Info",
        help_text="Add highlighted information in this section",
        max_length=65535,
        required=False,
    )
    alert = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        label="Alert",
        help_text="Add a highlighted alert that will display in this section",
        max_length=65535,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the section will appear on \
            the home page
            Lower values will appear first""",
        max_digits=8,
        initial=0,
    )
    hide_title = forms.BooleanField(
        help_text ="""Choose this option if you do not want \
            the title of this section to be displayed on the page""",
        required=False,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = HomePageSection
        fields = (
            'is_enabled',
            'members_only',
            'images',
            'title',
            'hide_title',
            'order',
            'text',
            'info',
            'alert',
            'sounds',
            'videos',
            'code',
            'links',
            'posts',
            'responses',
            'articles',
            'stories',
            'documents',
            'visuals',
            'galleries',
            'tracks',
            'albums',
        )
        help_texts = {
            'posts': """Choose one or more featured posts""",
            'responses': """Choose one or more featured responses""",
            'articles': """Choose one or more featured articles""",
            'stories': """Choose one or more featured stories""",
            'documents': """Choose one or more featured documents""",
            'visuals': """Choose one or more featured visuals""",
            'galleries': """Choose one or more featured galleries""",
            'tracks': """Choose one or more featured tracks""",
            'albums': """Choose one or more featured albums""",
            'sounds': """Choose one or more sounds""",
            'videos': """Choose one or more videos""",
            'code': """Choose one or more Code samples""",
            'links': """Choose one or more links""",
            'members_only': """Choose this option if you would like to \
                restrict the visibility of this section to members of \
                the site""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MemberProfileSectionForm, self).__init__(*args, **kwargs)
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
