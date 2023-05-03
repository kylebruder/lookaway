from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image, Sound, Video, Code, Link
from .models import MusicAppProfile, MusicPageSection, Album, Track

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

# App profile forms
class MusicAppProfileForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""The title will appear in the header
            It will also appear on search engine results pages (SERPs) and can 
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
        help_text="""Add a short description
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
        label="Blurb",
        help_text="Add a short blurb that will be displayed under the header",
        max_length=65535,
        required=False,
    )
    logo = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="""The logo will appear on the landing page and list headers
            The optimal image size is 250 pixels wide by 250 pixels high 
            (1:1)""",
    )
    banner = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="""The banner is the background image for the landing page 
            header
            The optimal image size is 1800 pixels wide by 400 pixels high 
            (9:2)""",
    )
    bg_image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        label="Background Image",
        help_text="The background image will appear on pages related to 
            this app",
    )
    n_tracks = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of tracks to show in each list on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_albums = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of albums to show in each list on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    track_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of tracks to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    album_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of albums to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_tracks = forms.BooleanField(
        label="Show the n newest tracks on the landing page",
        required=False,
    )
    show_top_tracks = forms.BooleanField(
        label="Show the top n tracks on the landing page",
        required=False,
    )
    show_new_albums = forms.BooleanField(
        label="Show the n newest albums on the landing page",
        required=False,
    )
    show_top_albums = forms.BooleanField(
        label="Show the top n albums on the landing page",
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = MusicAppProfile
        fields = (
            'title',
            'show_title',
            'meta_description',
            'show_desc',
            'text',
            'logo',
            'banner',
            'bg_image',
            'n_tracks',
            'n_albums',
            'track_list_pagination',
            'album_list_pagination',
            'show_new_tracks',
            'show_top_tracks',
            'show_new_albums',
            'show_top_albums',
            'links',
            'bitcoin_wallet',
            'litecoin_wallet',
        )
        help_texts = {
            'links': "Add featured links that will appear on the landing page.",
            'show_title': """Check this option if you would like the title to 
appear on the landing page header.""",
            'show_desc': """Check this option if you would like the 
meta description to appear on the landing page.""",
        }
        labels = {
            'show_desc': "Show description",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MusicAppProfileForm, self).__init__(*args, **kwargs)
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

class MusicPageSectionForm(forms.ModelForm):

    is_enabled = forms.BooleanField(
        label="Enabled",
        help_text="""Choose this option if you want this section to appear
            on the landing page""",
        required=False,
    )
    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more Images to include in this Section",
    )
    title = forms.CharField(
        help_text="""The section title will appear in the header of this 
            Section""",
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
        help_text="""Choose the order in which the section will appear on 
            the landing page
            Lower values will appear first""",
        max_digits=8,
        initial=0,
    )
    hide_title = forms.BooleanField(
        help_text ="""Choose this option if you do not want 
            the title of this section to be displayed on the page""",
        required=False,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = MusicPageSection
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
            'tracks',
            'albums',
            'sounds',
            'videos',
            'code',
            'links',
        )
        help_texts = {
            'sounds': """Choose one or more Sounds.""",
            'videos': """Choose one or more Videos.""",
            'code': """Choose one or more Code samples.""",
            'links': """Choose one or more Links.""",
            'members_only': """Choose this option if you would like to 
restrict the visibility of this section to members of 
the site.""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        if 'order' in kwargs:
            order = kwargs.pop('order')
            kwargs.update(initial={
                'order': order
            })
        super(MusicPageSectionForm, self).__init__(*args, **kwargs)
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
        self.fields['tracks'].queryset = Track.objects.filter(
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['albums'].queryset = Album.objects.filter(
            is_public=True,
        ).order_by(
            '-last_modified',
        )

class AlbumForm(forms.ModelForm):

    cover = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="Choose an iconic image as the cover for the Album",
        label="Cover Image",
    )
    title = forms.CharField(
        help_text="""The Album title will appear on the site and is used to 
            create the permanent URL for the Album  
            It will also appear on search engine results pages (SERPs) and 
            can impact search engine optimization (SEO)
            The optimal format is 'Primary Keyword - Secondary Keyword | 
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
            The description will be used by Search Engines and will impact 
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
            'cover': """Choose an image to represent the Album cover.
For best results use an image with a 1:1 aspect ratio. (optional)""",
            'links': """Add one or more links related the this Album.
Example: label website/band website/purchase options. (optional)""",
            'tags': "Add one or more tags.",
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
        help_text="""The Track title will appear on the site and is used to 
            create the permanent URL for the Track
            It will also appear on search engine results pages (SERPs) and can 
            impact search engine optimization (SEO)
            The optimal format is 'Primary Keyword - Secondary Keyword | Brand 
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
        help_text="""Choose the order in which the Track will appear in Track 
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
            'bitcoin_wallet',
            'litecoin_wallet',
        )
        help_texts = {
            'cover': """Choose an image to represent the Album cover.
For best results use an image with a 1:1 aspect ratio. (optional)""",
            'sound': "Select the Sound file for the Track.",
            'video': "Add a music video for the Track. (optional)",
            'links': """Add one or more links related the this Album.
Example: label website/band website/purchase options. (optional)""",
            'tags': "Add one or more tags. (optional)",
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        if 'sound' in kwargs:
            sound = Sound.objects.get(pk=kwargs.pop('sound'))
            if sound.credit:
                artist = sound.credit
            else:
                artist = sound.owner
            if sound.text:
                if len(sound.text) > 150:
                    description = "{}...".format(sound.text[:150])
                else:
                    description = sound.text
            else:
                description = "Fresh visual art by {}".format(artist)
            artist = sound.owner
            print(int(sound.pk))
            kwargs.update(initial={
                'sound': int(sound.pk),
                'title': sound.title,
                'meta_description': description,
                'text': sound.text,
                'artist': artist,
                'year': int(sound.creation_date.strftime('%Y'))
            })
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
