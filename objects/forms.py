from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from .models import ObjectsAppProfile, ObjectsPageSection, Image, Sound, Video, Code, Link, Tag 

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

# Object app profile form
class ObjectsAppProfileForm(forms.ModelForm):

    title = forms.CharField(
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
        help_text="""Add a short description.
The description will be used by Search Engines and will impact SEO.
Include key words used in the title.
Keep it less than 155 characters.""",
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
        help_text="Add a short blurb that will be displayed under the header.",
        max_length=65535,
        required=False,
    )
    logo = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="""The logo will appear on the landing page and list headers.
The optimal image size is 250 pixels wide by 250 pixels high (1:1).""",
    )
    banner = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="""The banner is the background image for the landing page header.
The optimal image size is 1800 pixels wide by 400 pixels high (9:2).""",
    )
    bg_image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        label="Background Image",
        help_text="The background image will appear on pages related to this app.",
    )
    n_images = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of images to show on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_sounds = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of sounds to show on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_videos = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of videos to show on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_codes = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of code samples to show on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_links = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of links to show on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    images_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of images to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    sounds_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of sounds to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    videos_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of videos to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    codes_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of code samples to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    links_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of links to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_images = forms.BooleanField(
        label="Show the top n images on the landing page",
        required=False,
    )
    show_sounds = forms.BooleanField(
        label="Show the top n sounds on the landing page",
        required=False,
    )
    show_videos = forms.BooleanField(
        label="Show the top n videos on the landing page",
        required=False,
    )
    show_codes = forms.BooleanField(
        label="Show the top n code samples on the landing page",
        required=False,
    )
    show_links = forms.BooleanField(
        label="Show the top n links on the landing page",
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = ObjectsAppProfile
        fields = (
            'title',
            'show_title',
            'meta_description',
            'show_desc',
            'text',
            'logo',
            'banner',
            'bg_image',
            'n_images',
            'n_sounds',
            'n_videos',
            'n_codes',
            'n_links',
            'images_list_pagination',
            'sounds_list_pagination',
            'videos_list_pagination',
            'codes_list_pagination',
            'links_list_pagination',
            'show_images',
            'show_sounds',
            'show_videos',
            'show_codes',
            'show_links',
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
        super(ObjectsAppProfileForm, self).__init__(*args, **kwargs)
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

class ObjectsAppTranscoderSettingsForm(forms.ModelForm):

    # Available Formats
    IMAGE_FORMAT_CHOICES = [
        ('WEBP', 'webp'),
        ('JPG', 'jpg'),
    ]
    SOUND_FORMAT_CHOICES = [
        ('OGG', 'ogg'),
        ('MP3', 'mp3'),
    ]
    VIDEO_FORMAT_CHOICES = [
        ('WEBM', 'webm'),
        ('MP4', 'mp4'),
    ]

    ffmpeg_path = forms.CharField(
        help_text="""Specify the path to the ffmpeg binary. 
You must have ffmpeg installed in order to transcode
sound and video files.""",
        max_length=128,
    )
    image_format = forms.CharField(
        help_text="""Choose the format which will be used to 
transcode uploaded image files.""",
        max_length=128,
        widget=forms.Select(
            choices=IMAGE_FORMAT_CHOICES,
            attrs={
                'class': 'form-text-field',
            },
        ),
    )
    image_max_height = forms.IntegerField(
        max_value=7000,
        min_value=250,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    image_max_width = forms.IntegerField(
        max_value=7000,
        min_value=250,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    thumbnail_max_height = forms.IntegerField(
        max_value=7000,
        min_value=250,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    thumbnail_max_width = forms.IntegerField(
        max_value=7000,
        min_value=250,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    sound_format = forms.CharField(
        help_text="""Choose the format which will be used to 
transcode uploaded sound files.""",
        max_length=128,
        widget=forms.Select(
            choices=SOUND_FORMAT_CHOICES,
            attrs={
                'class': 'form-text-field',
            },
        ),
    )
    video_format = forms.CharField(
        help_text="""Choose the format which will be used to 
transcode uploaded video files.""",
        max_length=128,
        widget=forms.Select(
            choices=VIDEO_FORMAT_CHOICES,
            attrs={
                'class': 'form-text-field',
            },
        ),
    )
    sound_bitrate = forms.IntegerField(
        max_value=10**8,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    video_bitrate = forms.IntegerField(
        max_value=10**8,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    sound_crf = forms.IntegerField(
        max_value=10**8,
        min_value=0,
        label="""Audio Constant Rate Factor""",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    video_crf = forms.IntegerField(
        max_value=10**8,
        min_value=0,
        label="""Video Constant Rate Factor""",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )

    ffmpeg_path.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = ObjectsAppProfile
        fields = (
            'ffmpeg_path',
            'image_format',
            'image_max_height',
            'image_max_width',
            'thumbnail_max_height',
            'thumbnail_max_width',
            'sound_format',
            'sound_bitrate',
            'sound_crf',
            'video_format',
            'video_bitrate',
            'video_crf',
        )
        help_texts = {
            'links': "Add featured links that will appear on the landing page.",
            'show_title': """Check this option if you would like the title to 
appear on the landing page heade.r""",
            'show_desc': """Check this option if you would like the 
meta description to appear on the landing page.""",
            'sound_crf': """Higher values mean more compression, 
but at some point you will notice quality degradation.""",
            'video_crf': """Higher values mean more compression, 
but at some point you will notice quality degradation.""",
            'sound_bitrate': """Number of kilobytes per second.""",
            'video_bitrate': """Number of kilobytes per second."""
        },
        labels = {
            'show_desc': "Show description",
        }

class ObjectsPageSectionForm(forms.ModelForm):

    is_enabled = forms.BooleanField(
        label="Enabled",
        help_text="""Choose this option if you want this section to appear
on the landing page.""",
        required=False,
    )
    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more Images to include in this Section.",
    )
    title = forms.CharField(
        help_text="""The section title will appear in the header of this Section.""",
        max_length=255,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Enter the section text here.",
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
the landing page.
Lower values will appear first.""",
        max_digits=8,
        initial=0,
    )
    hide_title = forms.BooleanField(
        help_text ="""Choose this option if you do not want 
the title of this section to be displayed on the page.""",
        required=False,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = ObjectsPageSection
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
        )
        help_texts = {
            'sounds': """Choose one or more sounds.""",
            'videos': """Choose one or more videos.""",
            'code': """Choose one or more code samples.""",
            'links': """Choose one or more links.""",
            'members': """Choose one or more members to feature.""",
            'members_only': """Choose this option if you would like to 
restrict the visibility of this section to members of the site.""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        # Populate order field
        if 'order' in kwargs:
            bar = kwargs.pop('order')
            kwargs.update(initial={
                'order': bar
            })
        super(ObjectsPageSectionForm, self).__init__(*args, **kwargs)
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

class ImageCreateForm(forms.ModelForm):

    # Remove comment lines to allow adding these fields on creation form.
    '''
    title = forms.CharField(
        help_text="""Give the Image a memorable and unique title that will be 
easy to reference later.""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""The Image text may appear on pages that include Images.""",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the image file.
Obtain expressed permission before uploading images with exclusive rights.""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})
    '''

    class Meta:
        model = Image
        fields = [
            'image_file',
            #'title',
            #'text',
            #'credit',
            #'tags',
        ]
        widgets = {
            'image_file': ImagePreviewWidget
        }
        help_texts = {
            'image_file': """Obtain permission before uploading depicitons of 
private persons or places.
Image Preview will appear when successfully uploaded.""",
            'tags': "Choose one or more tags.",
        }

class ImageUpdateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Image a memorable and unique title that will be 
easy to reference later.""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""The Image text may appear on pages that include Images.""",
        max_length=1024,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the image will appear. 
Lower values will appear first.""",
        max_digits=8,
        initial=0,
    )
    credit = forms.CharField(
        max_length=256,
        help_text="""Give credit to the original creator of the image file
Obtain expressed permission before uploading images with exclusive rights.""",
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    order.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Image
        fields = [
            'title',
            'text',
            'order',
            'credit',
            'tags',
        ]
        help_texts = {
            'tags': "Choose one or more tags.",
        }

class SoundCreateForm(forms.ModelForm):

    # Remove comment lines to allow adding these fields on creation form.
    '''
    title = forms.CharField(
        help_text="""Give the Sound a memorable and unique title that will be 
easy to reference later.""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Images.",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Sound file.
Obtain expressed permission before uploading sounds with exclusive rights.""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})
    '''
    class Meta:
        model = Sound
        fields = [
            'sound_file',
            #'title',
            #'text',
            #'credit',
            #'tags',
        ]
        widgets = {
            'sound_file': SoundPreviewWidget
        }
        help_texts = {
            'sound_file': """Obtain permission before uploading depicitons of 
private persons or places.
Sound Preview will appear when successfully uploaded.""",
            'tags': "Choose one or more tags.",
        }

class SoundUpdateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Sound a memorable and unique title that will be 
easy to reference later.""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Images.",
        max_length=1024,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the sound will appear. 
Lower values will appear first.""",
        max_digits=8,
        initial=0,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Sound file.
Obtain expressed permission before uploading sounds with exclusive 
rights.""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    order.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Sound
        fields = [
            'title',
            'text',
            'order',
            'credit',
            'tags',
        ]
        help_texts = {
            'tags': "Choose one or more tags.",
        }

class VideoCreateForm(forms.ModelForm):

    # Remove comment lines to allow adding these fields on creation form.
    '''
    title = forms.CharField(
        help_text="""Give the Video memorable and unique title that will be easy 
to reference later.""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Images.",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Video file.
Obtain expressed permission before uploading videos with exclusive rights.""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})
    '''
    class Meta:
        model = Video
        fields = [
            'video_file',
            #'title',
            #'text',
            #'credit',
            #'tags',
        ]
        widgets = {
            'video_file': VideoPreviewWidget
        }

        help_texts = {
            'video_file': """Obtain permission before uploading depicitons of 
private persons or places.
Video Preview will appear when successfully uploaded.""",
            'tags': "Choose one or more tags.",
        }

class VideoUpdateForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Video memorable and unique title that will be easy 
to reference later.""",
        max_length=64,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Videos.",
        max_length=1024,
        required=False,
    )
    credit = forms.CharField(
        help_text="""Give credit to the original creator of the Video file.
Obtain expressed permission before uploading videos with exclusive rights.""",
        max_length=256,
        required=False,
    )

    title.widget.attrs.update({'class': 'form-text-field'})
    order = forms.DecimalField(
        help_text="""Choose the order in which the video will appear. 
Lower values will appear first.""",
        max_digits=8,
        initial=0,
    )
    order.widget.attrs.update({'class': 'form-text-field'})
    credit.widget.attrs.update({'class': 'form-text-field'})


    class Meta:
        model = Video
        fields = [
            'title',
            'text',
            'order',
            'credit',
            'tags',
        ]
        help_texts = {
            'tags': "Choose one or more tags.",
        }


class CodeForm(forms.ModelForm):

    title = forms.CharField(
        help_text="""Give the Code sample a memorable and unique title that will 
be easy to reference later.""",
        max_length=256,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Include comments with your Code. (optional)",
        label="Comments",
        max_length=1024,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the code will appear. 
Lower values will appear first.""",
        max_digits=8,
        initial=0,
    )
    code = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'wrap': 'off',
                'class': 'code-block form-text-field',
            }
        ),
        help_text="Enter the code here.",
        max_length=65535,
    )
    language= forms.CharField(
        help_text="For which language is the code written?",
        max_length=64,
    )
    language_version= forms.CharField(
        help_text="""For which version or versions of the language is the code 
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
Please credit yourself or your source. (optional)""",
        max_length=64,
        required=False,
    )
    source_url = forms.CharField(
        help_text="""Does the source have a website or webpage?
If so enter it here. (optional)""",
        max_length=256,
        required=False,
    )

    order.widget.attrs.update({'class': 'form-text-field'})
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
            'order',
            'tags',
        ]
        widgets = {
            'code': Textarea(attrs={
                'wrap': 'off',
                'class': 'code-block',
            }),
        }
        help_texts = {
            'tags': "Choose one or more tags.",
        }

class LinkCreateForm(forms.ModelForm):

    url = forms.CharField(
        help_text="Enter the URL here.",
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
        help_text="""Give the Link a memorable and unique title that will be 
easy to reference later.""",
        max_length=256,
        required=False,
    )
    url = forms.CharField(
        help_text="Enter the URL here.",
        max_length=256,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="The text may appear on pages that include Links.",
        max_length=512,
        required=False,
    )
    favicon_href = forms.CharField(
        help_text="Enter a URL for the webpage image.",
        max_length=256,
        required=False,
    )
    order = forms.DecimalField(
        help_text="""Choose the order in which the link will appear. 
Lower values will appear first.""",
        max_digits=8,
        initial=0,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    text.widget.attrs.update({'class': 'form-text-field'})
    url.widget.attrs.update({'class': 'form-text-field'})
    favicon_href.widget.attrs.update({'class': 'form-text-field'})
    order.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Link
        fields = [
            'title',
            'url',
            'text',
            'favicon_href',
            'order',
            'tags',
        ]
        help_texts = {
            'tags': "Choose one or more tags.",
        }

class TagForm(forms.ModelForm):

    key = forms.CharField(
        help_text="Enter a word or words that describe a category.",
        max_length=64,
    )
    value = forms.CharField(
        help_text="""Enter words or numbers that describe a qualitative or 
quantitative value.""",
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
