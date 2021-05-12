from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image, Sound, Video, Code, Link
from .models import ArtAppProfile, ArtPageSection, Gallery, Visual

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

# Art app profile form
class ArtAppProfileForm(forms.ModelForm):

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
            The optimal image size is 250 pixels wide by 250 pixels high \
            (1:1)""",
    )
    banner = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        help_text="""The banner is the background image for the landing page \
            header
            The optimal image size is 1800 pixels wide by 400 pixels high \
            (9:2)""",
    )
    bg_image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        label="Background Image",
        help_text="The background image will appear on pages related to \
            this app",
    )
    n_visuals = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of visuals to show in each list on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_galleries = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of galleries to show in each list on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    visual_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of visuals to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    gallery_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of galleries to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_visuals = forms.BooleanField(
        label="Show the n newest visuals on the landing page",
        required=False,
    )
    show_top_visuals = forms.BooleanField(
        label="Show the top n visuals on the landing page",
        required=False,
    )
    show_new_galleries = forms.BooleanField(
        label="Show the n newest galleries on the landing page",
        required=False,
    )
    show_top_galleries = forms.BooleanField(
        label="Show the top n galleries on the landing page",
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = ArtAppProfile
        fields = (
            'title',
            'show_title',
            'meta_description',
            'show_desc',
            'text',
            'logo',
            'banner',
            'bg_image',
            'n_visuals',
            'n_galleries',
            'visual_list_pagination',
            'gallery_list_pagination',
            'show_new_visuals',
            'show_top_visuals',
            'show_new_galleries',
            'show_top_galleries',
            'links',
            'bitcoin_wallet',
            'litecoin_wallet',
        )
        help_texts = {
            'links': "Add featured links that will appear on the landing page",
            'show_title': """Check this option if you would like the title to \
                appear on the landing page header""",
            'show_desc': """Check this option if you would like the \
                meta description to appear on the landing page""",
        }
        labels = {
            'show_desc': "Show description",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ArtAppProfileForm, self).__init__(*args, **kwargs)
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

# Art page section form
class ArtPageSectionForm(forms.ModelForm):

    is_enabled = forms.BooleanField(
        label="Enabled",
        help_text="""Choose this option if you want this section to appear\
            on the landing page""",
        required=False,
    )
    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more images",
    )
    visuals = CustomModelMultipleChoiceField(
        queryset = Visual.objects.all(),
        required=False,
        help_text="Choose one or more visuals to feature in this section",
    )
    title = forms.CharField(
        help_text="""The section title will appear in the header of this \
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
        help_text="""Choose the order in which the section will appear on \
            the landing page
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
        model = ArtPageSection
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
            'visuals',
            'galleries',
            'sounds',
            'videos',
            'code',
            'links',
        )
        help_texts = {
            'sounds': """Choose one or more sounds""",
            'videos': """Choose one or more videos""",
            'code': """Choose one or more code samples""",
            'links': """Choose one or more links""",
            'galleries': """Choose one or more galleries \
                to feature in this section""",
            'members_only': """Choose this option if you would like to \
                restrict the visibility of this section to members of \
                the site""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ArtPageSectionForm, self).__init__(*args, **kwargs)
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
        self.fields['visuals'].queryset = Visual.objects.filter(
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['galleries'].queryset = Gallery.objects.filter(
            is_public=True,
        ).order_by(
            '-last_modified',
        )

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
            'bitcoin_wallet',
            'litecoin_wallet',
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
        self.fields['video'].queryset = Video.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
        self.fields['visuals'].queryset = Visual.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
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
    dimensions = forms.CharField(
        help_text="""Provide measurements such as length, width, diameter or \
            weight.""",
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
    dimensions.widget.attrs.update({'class': 'form-text-field'})
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
            'dimensions',
            'credits',
            'year',
            'links',
            'tags',
            'bitcoin_wallet',
            'litecoin_wallet',
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
        if 'image' in kwargs:
            image = Image.objects.get(pk=kwargs.pop('image'))
            if image.credit:
                artist = image.credit
            else:
                artist = image.owner
            if image.text:
                if len(image.text) > 150:
                    description = "{}...".format(image.text[:150])
                else:
                    description = image.text
            else:
                description = "Fresh visual art by {}".format(artist)
            artist = image.owner
            print(int(image.pk))
            kwargs.update(initial={
                'image': int(image.pk),
                'title': image.title,
                'meta_description': description,
                'text': image.text,
                'artist': artist,
                'year': int(image.creation_date.strftime('%Y'))
            })
        super(VisualForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
        self.fields['video'].queryset = Video.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )
