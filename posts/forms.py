from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image, Sound, Video, Code
from .models import PostsAppProfile, PostsPageSection, Post, ResponsePost, ReportPost

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

# Posts app profile form
class PostsAppProfileForm(forms.ModelForm):

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
    n_posts = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of posts to show in each list on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_responses = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of responses to show in each list on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    post_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of posts to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    response_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of responses to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_posts = forms.BooleanField(
        label="Show the n newest posts on the landing page",
        required=False,
    )
    show_top_posts = forms.BooleanField(
        label="Show the top n posts on the landing page",
        required=False,
    )
    show_new_responses = forms.BooleanField(
        label="Show the n newest responses on the landing page",
        required=False,
    )
    show_top_responses = forms.BooleanField(
        label="Show the top n responses on the landing page",
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = PostsAppProfile
        fields = (
            'title',
            'show_title',
            'meta_description',
            'show_desc',
            'text',
            'logo',
            'banner',
            'bg_image',
            'n_posts',
            'n_responses',
            'post_list_pagination',
            'response_list_pagination',
            'show_new_posts',
            'show_top_posts',
            'show_new_responses',
            'show_top_responses',
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
        super(PostsAppProfileForm, self).__init__(*args, **kwargs)
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
class PostsPageSectionForm(forms.ModelForm):

    is_enabled = forms.BooleanField(
        label="Enabled",
        help_text="""Choose this option if you want this section to appear\
            on the landing page""",
        required=False,
    )
    images = CustomModelMultipleChoiceField(
        queryset = Image.objects.all(),
        required=False,
        help_text="Choose one or more Images to include in this Section",
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
        model = PostsPageSection
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
            'posts',
            'sounds',
            'videos',
            'code',
            'links',
        )
        help_texts = {
            'sounds': """Choose one or more Sounds""",
            'videos': """Choose one or more Videos""",
            'code': """Choose one or more Code samples""",
            'links': """Choose one or more Links""",
            'members_only': """Choose this option if you would like to \
                restrict the visibility of this section to members of \
                the site""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PostsPageSectionForm, self).__init__(*args, **kwargs)
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
        self.fields['posts'].queryset = Post.objects.filter(
            is_public=True,
        ).order_by(
            '-last_modified',
        )

class PostForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
    )
    title = forms.CharField(
        help_text="""The Post title will appear on the site and is used to \
            create the permanent URL for this Post
            It will also appear on search engine results pages (SERPs) and can \
            impact search engine optimization (SEO)
            The optimal format is 'Primary Keyword - Secondary Keyword | \
            Brand Name'""",
        max_length=128,
    )
    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of this post
            This description will be used by search engines and will impact SEO
            Include key words used in the title
            Keep it less than 155 characters""",
        max_length=155,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Your message to the world goes here",
        max_length=65535,
    )
    location = forms.CharField(
        help_text="Where are you posting from? (optional)",
        max_length=128,
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    location.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Post
        fields = (
            'title',
            'meta_description',
            'text',
            'location',
            'image',
            'sound',
            'video',
            'code',
            'link',
            'tags',
            'bitcoin_wallet',
            'litecoin_wallet',
            'members_only',
        )
        help_texts = {
            'image': "Add an Image (optional)",
            'sound': "Add a Sound (optional)",
            'video': "Add a Video (optional)",
            'code': "Add Code (optional)",
            'link': "Add a Link (optional)",
            're': """Is this post a response to another post?
                If so select a post here""",
            'members_only': """If this option is checked only Members will \
                be able to view your post after publication
                Unchecking this option will make your post public to the \
                world""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
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
        self.fields['code'].queryset = Code.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class ResponsePostForm(forms.ModelForm):

    image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
    )
    title = forms.CharField(
        help_text="""The Response title will appear on the site and is used to \
            create the permanent URL for this Response
            It will also appear on search engine results pages (SERPs) and can \
            impact search engine optimization (SEO)""",
        max_length=128,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Your response message goes here",
        max_length=65535,
    )
    location = forms.CharField(
        help_text="Where are you responding from? (optional)",
        max_length=128,
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})
    location.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = ResponsePost
        fields = (
            'title',
            'text',
            'location',
            'image',
            'sound',
            'video',
            'code',
            'link',
            'tags',
        )
        help_texts = {
            'image': "Add an Image (optional)",
            'sound': "Add a Sound (optional)",
            'video': "Add a Video (optional)",
            'code': "Add Code (optional)",
            'link': "Add a Link (optional)",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ResponsePostForm, self).__init__(*args, **kwargs)
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
        self.fields['code'].queryset = Code.objects.filter(
            owner=user.pk,
        ).order_by(
            '-last_modified',
        )

class ReportPostForm(forms.ModelForm):

    title = forms.CharField(
        help_text="Please provide a title for this report",
        max_length=128,
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        label="Report",
        help_text="""Please let us know which part of our content should be \
            submitted for review""",
        max_length=65535,
    )
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = ReportPost
        fields = (
            'title',
            'text',
        )
