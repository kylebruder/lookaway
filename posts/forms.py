from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image, Sound, Video, Code
from .models import Post

class CustomModelChoiceIterator(forms.models.ModelChoiceIterator):

    def choice(self, obj):
        return self.field.prepare_value(obj), self.field.label_from_instance(obj), obj

class CustomModelChoiceField(forms.models.ModelChoiceField):

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)

    choices = property(_get_choices, forms.ChoiceField._set_choices)

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
            're',
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
