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

class SiteProfileForm(forms.ModelForm):

    nav_show_posts = forms.BooleanField(
        label="Show a link to the Posts app in the navbar.",
        required=False,
    )
    nav_posts_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set the name of the Posts app in the navbar.""",
        max_length=64,
    )
    nav_show_documentation = forms.BooleanField(
        label="Show a link to the Documentation app in the navbar.",
        required=False,
    )
    nav_documentation_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set the name of the Documentation app in the navbar.""",
        max_length=64,
    )
    nav_show_art = forms.BooleanField(
        label="Show a link to the Art app in the navbar.",
        required=False,
    )
    nav_art_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set the name of the Art app in the navbar.""",
        max_length=64,
    )
    nav_show_music = forms.BooleanField(
        label="Show a link to the Music app in the navbar.",
        required=False,
    )
    nav_music_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set the name of the Music app in the navbar.""",
        max_length=64,
    )
    nav_show_members = forms.BooleanField(
        label="Show a link to the Members app in the navbar.",
        required=False,
    )
    nav_members_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set the name of the Members app in the navbar.""",
        max_length=64,
    )
    nav_show_objects = forms.BooleanField(
        label="Show a link to the Objects app in the navbar.",
        required=False,
    )
    nav_objects_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set the name of the Objects app in the navbar.""",
        max_length=64,
    )
    legal_notice = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a notice that will appear in the footer 
on every page.""",
        max_length=155,
        label="Legal Notice",
        required=False,
    )
    admin_email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set a contact email that will appear in the footer 
on every page.""",
        max_length=64,
        label = "Admin Contact Email",
        required=False,
    )
    css_path = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Set an alternate css file. Enter a relative path 
starting with a '/'. Leaving this field blank will use the 
default Lookaway CSS. There path you provide is not validated. 
If the provided path is unavailable, most browsers will fail 
silently and may result in no styling at all. This setting can 
also be changed in the Django admin panel.
Example: '/static/my_style.css'.""",
        max_length=64,
        label = "Alternative CSS",
        required=False,
    )

    class Meta:
        model = HomeAppProfile
        fields = (
            'nav_show_posts',
            'nav_posts_name',
            'nav_posts_image',
            'nav_show_documentation',
            'nav_documentation_name',
            'nav_documentation_image',
            'nav_show_art',
            'nav_art_name',
            'nav_art_image',
            'nav_show_music',
            'nav_music_name',
            'nav_music_image',
            'nav_show_members',
            'nav_members_name',
            'nav_members_image',
            'nav_show_objects',
            'nav_objects_name',
            'nav_objects_image',
            'legal_notice',
            'admin_email',
            'css_path',
        )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SiteProfileForm, self).__init__(*args, **kwargs)
        self.fields['nav_posts_image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['nav_documentation_image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['nav_art_image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['nav_music_image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['nav_members_image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )


class HomeAppProfileForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""The title will appear in the header. 
It will also appear on search engine results pages (SERPs) and can 
impact search engine optimization (SEO).""",
        max_length=128,
        required=False,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of the website. 
The description will be used by Search Engines and will impact SEO. 
Include key words used on your page. 
Keep it less than 155 characters.""",
        max_length=155,
        required=False,
    )
    logo = CustomModelChoiceField(
        queryset=Image.objects.all(),
        help_text="Choose your site's logo image.",
        required=False, 
        label="Logo",
    )
    banner = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="""The banner is the background image for the home page 
header. The optimal image size is 1800 pixels wide by 400 pixels high (9:2).""",
    )
    bg_image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        label="Background Image",
        help_text="The background image will appear on the home page."
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Add a short blurb which will be displayed under the header.",
        required=False, 
        label="Blurb (optional)",
    )

    class Meta:
        model = HomeAppProfile
        fields = (
            'logo',
            'banner',
            'bg_image',
            'title',
            'meta_description',
            'text',
            'links',
            'bitcoin_wallet',
            'litecoin_wallet',
        )
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(HomeAppProfileForm, self).__init__(*args, **kwargs)
        self.fields['logo'].queryset = Image.objects.filter(
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
        help_text="""Choose this option if you want this section to appear
on the home page.""",
        required=False,
    )
    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more images to include in this section.",
    )
    visuals = CustomModelMultipleChoiceField(
        queryset = Visual.objects.all(),
        required=False,
        help_text="Choose one or featured visuals in this section.",
    )
    title = forms.CharField(
        help_text="""The section title will appear in the header of this 
section.""",
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
        help_text="Add highlighted information in this section.",
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
        help_text="Add a highlighted alert that will display in this section.",
        max_length=65535,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the section will appear on 
the home page. 
Lower values will appear first.""",
        max_digits=8,
    )
    hide_title = forms.BooleanField(
        help_text ="""Choose this option if you do not want 
the title of this section to be displayed on the page.""",
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
            'posts': """Choose one or more featured posts.""",
            'responses': """Choose one or more featured responses.""",
            'articles': """Choose one or more featured articles.""",
            'stories': """Choose one or more featured stories.""",
            'documents': """Choose one or more featured documents.""",
            'galleries': """Choose one or more featured galleries.""",
            'tracks': """Choose one or more featured tracks.""",
            'albums': """Choose one or more featured albums.""",
            'sounds': """Choose one or more sounds.""",
            'videos': """Choose one or more videos.""",
            'code': """Choose one or more code samples.""",
            'links': """Choose one or more links.""",
            'members_only': """Choose this option if you would like to 
restrict the visibility of this section to members of 
the site.""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        if 'order' in kwargs:
            order = kwargs.pop('order')
            kwargs.update(initial={
                'order': order,
            })
        super(HomePageSectionForm, self).__init__(*args, **kwargs)
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
