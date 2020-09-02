from django import forms
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.models import Member
from objects.models import Image
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

    class Meta:
        model = Post
        fields = (
            'title',
            'meta_description',
            'location',
            'text',
            'image',
            'sound',
            'video',
            'code',
            'link',
            'tags',
            're',
            'members_only',
        )
        help_texts = {
            'title': "Get attention with one clever and consise sentence. The headline will be displayed on search engine results pages (SERPs) and will improve search engine optimization (SEO). The optimal format is 'Primary Keyword - Secondary Keyword | Brand Name'.",
            'meta_description': "Add a short description of this post. This description will be used by Search Engines and will improve optimization. Include key words used in the title. Keep it less than 155 characters.",
            'location': "Where are you posting from? (optional)",
            'text': "Here is where you type your message.",
            'image': "Add an Image (optional)",
            'sound': "Add a Sound (optional)",
            'video': "Add a Video (optional)",
            'code': "Add Code (optional)",
            'link': "Add a Link (optional)",
            're': "Is this post a response to another post? If so select a post here.",
            'members_only': "If this option is checked only other members will be able to view your post after publication.",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.filter(
            owner=user.pk,
        ).order_by(
            '-creation_date',
        )
