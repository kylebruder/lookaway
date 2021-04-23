from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Textarea
from templates.widgets import ImagePreviewWidget, SoundPreviewWidget, VideoPreviewWidget
from members.bad_names import bad_names
from art.models import Visual, Gallery
from documentation.models import Article, Story, SupportDocument
from music.models import Track, Album
from objects.models import Image, Sound, Video, Code, Link
from .models import Member, MembersAppProfile, MembersPageSection, Profile, MemberProfileSection, InviteLink 

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

class UserRegistrationForm(UserCreationForm):

    username = forms.CharField(
        label="Member Login",
        max_length=32,
        help_text="""Use only lower case letters in your Member Login \
            Name. Your Member Login name is used to create a permanent URL for \
            your Profile page and is also used to credit \
            your contributions unless you choose a display name or provide \
            a first and last name.""",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Verify Password",
        )
    first_name = forms.CharField(
        widget=forms.PasswordInput(),
        label="First Name (optional)",
        help_text="""You may use your real name or an alias or completely fake \
            name.""",
        required=False,
    )
    last_name = forms.CharField(
        widget=forms.PasswordInput(),
        label="Last Name (optional)",
        help_text="""If you provide a first AND last name, they will be used  \
            to credit your contributions unless you choose a display name for \
            your Profile after creating your Member account.""",
        required=False,
    )
    email = forms.CharField(
        widget=forms.EmailInput(),
        label="Recovery Email (optional)",
        help_text="""If you provide an email contact, your email address will \
            only be used to recover your password in the event you no longer \
            know you password. IMPORTANT! If you do not provide an valid \
            email address, you will be unable to use the Password Recovery \
            Service. We do not confirm whether or not your recovery email \
            address is valid so be sure you have can access the email address \
            you provide. The recovery email can be changed any time as long \
            as you are authenticated to the site.""",
        required=False,
    )
    username.widget.attrs.update({'class': 'form-text-field'})
    password1.widget.attrs.update({'class': 'form-text-field'})
    password2.widget.attrs.update({'class': 'form-text-field'})
    first_name.widget.attrs.update({'class': 'form-text-field'})
    last_name.widget.attrs.update({'class': 'form-text-field'})
    email.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
        )

    # Thanks to Junior Mayta
    # https://stackoverflow.com/questions/52723824/how-to-create-a-validator-for-special-characters-in-django?rq=1
    def validate_username(self, string):
        '''
        Ensure the supplied username only contains lowercase letters and numbers
        Pass cleaned form data as a string
        returns either True or False
        '''
        for char in string:
            if not char.isdigit() and not char.isalpha():
                return False
        '''
        Members Choose their names during registration.
        A valid name is used as the slug for their profile page.
        In order to allow short profile URLs, with the member name
        after the FQDN, we need to make sure no one has the same name
        as any slug in the paths in lookaway.urls.
        Returns a list of blacklisted names.
        ''' 
        for x in bad_names:
            if string in x:
                return False
        return True

    def clean_username(self):
        data = self.cleaned_data['username']
        if not data.islower():
            raise forms.ValidationError("Your username may only include lowercase letters.")
        if not self.validate_username(data):
            raise forms.ValidationError("Your username may only include letters and numbers.")
        return data
            
class MemberForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=30,
        required=False,
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
    )
    email = forms.CharField(
        required=False,
    )
    first_name.widget.attrs.update({'class': 'form-text-field'})
    last_name.widget.attrs.update({'class': 'form-text-field'})
    email.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Member
        fields = (
            'first_name',
            'last_name',
            'email',
        )

class MembersPageSectionForm(forms.ModelForm):

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
        model = MembersPageSection
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
            'members',
        )
        help_texts = {
            'sounds': """Choose one or more sounds""",
            'videos': """Choose one or more videos""",
            'code': """Choose one or more code samples""",
            'links': """Choose one or more links""",
            'members': """Choose one or more members to feature""",
            'members_only': """Choose this option if you would like to \
                restrict the visibility of this section to members of \
                the site""",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MembersPageSectionForm, self).__init__(*args, **kwargs)
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

# Members app profile form
class MembersAppProfileForm(forms.ModelForm):

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
    n_members = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of members to show on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_bars = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of contributors to show on the landing page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    member_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of foos to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    contributor_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of bars to show in lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_members = forms.BooleanField(
        label="Show the n newest members on the landing page",
        required=False,
    )
    show_contributors = forms.BooleanField(
        label="Show the n newest contributors on the landing page",
        required=False,
    )
    title.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = MembersAppProfile
        fields = (
            'title',
            'show_title',
            'meta_description',
            'show_desc',
            'text',
            'logo',
            'banner',
            'bg_image',
            'n_members',
            'n_contributors',
            'member_list_pagination',
            'contributors_list_pagination',
            'show_members',
            'show_contributors',
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
        super(MembersAppProfileForm, self).__init__(*args, **kwargs)
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

class ProfileForm(forms.ModelForm):

    meta_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="""Add a short description of your profile page \
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
        help_text="""The banner is the background image for your profile page \
            header
            The optimal image size is 1800 pixels wide by 400 pixels high \
            (9:2)""",
    )
    bg_image = CustomModelChoiceField(
        queryset=Image.objects.all(),
        required=False, 
        label="Background Image",
        help_text="The background image will appear on your profile page \
            and lists of your contributions",
    )
    display_name = forms.CharField(
        max_length=64,
        help_text="""Your display name is shown on your profile page and is \
            used to credit your contributions.""",
        required=False,
        label="Display Name (optional)",
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        help_text="Explain yourself here.",
        required=False, 
        label="Blurb (optional)",
    )
    display_name.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = Profile
        fields = (
            'image',
            'display_name',
            'meta_description',
            'text',
            'banner',
            'bg_image',
            'show_email',
        )
        help_texts = {
            'show_email': """Choose this option if you have already provided \
                an email address and you would like your email address \
                to appear on your profile page""",
        }
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

class ProfileSettingsForm(forms.ModelForm):
    show_new_posts = forms.BooleanField(
        label="Show the n newest posts on your profile page",
        required=False,
    )
    show_top_posts = forms.BooleanField(
        label="Show the top n posts on the your profile page",
        required=False,
    )
    show_new_responses = forms.BooleanField(
        label="Show the n newest responses on your profile page",
        required=False,
    )
    show_top_responses = forms.BooleanField(
        label="Show the top n responses on your profile page",
        required=False,
    )
    n_posts = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of posts to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_responses = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of responses to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    post_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of posts to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    response_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of responses to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_articles = forms.BooleanField(
        label="Show the n newest articles on your profile page",
        required=False,
    )
    show_top_articles = forms.BooleanField(
        label="Show the top n articles on your profile page",
        required=False,
    )
    show_new_stories = forms.BooleanField(
        label="Show the n newest stories on your profile page",
        required=False,
    )
    show_top_stories = forms.BooleanField(
        label="Show the top n stories on your profile page",
        required=False,
    )
    show_new_support_documents = forms.BooleanField(
        label="Show the n newest documents on your profile page",
        required=False,
    )
    show_top_support_documents = forms.BooleanField(
        label="Show the top n documents on your profile page",
        required=False,
    )
    n_articles = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of articles to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_stories = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of stories to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_documents = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of documents to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    article_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of articles to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    story_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of stories to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    document_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of documents to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_visuals = forms.BooleanField(
        label="Show the n newest visuals on your profile page",
        required=False,
    )
    show_top_visuals = forms.BooleanField(
        label="Show the top n visuals on your profile page",
        required=False,
    )
    show_new_galleries = forms.BooleanField(
        label="Show the n newest galleries on your profile page",
        required=False,
    )
    show_top_galleries = forms.BooleanField(
        label="Show the top n galleries on your profile page",
        required=False,
    )
    n_visuals = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of visuals to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_galleries = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of galleries to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    visual_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of visuals to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    gallery_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of galleries to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    show_new_tracks = forms.BooleanField(
        label="Show the n newest tracks on your profile page",
        required=False,
    )
    show_top_tracks = forms.BooleanField(
        label="Show the top n tracks on your profile page",
        required=False,
    )
    show_new_albums = forms.BooleanField(
        label="Show the n newest albums on your profile page",
        required=False,
    )
    show_top_albums = forms.BooleanField(
        label="Show the top n albums on your profile page",
        required=False,
    )
    n_tracks = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of tracks to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    n_albums = forms.IntegerField(
        max_value=1000,
        min_value=0,
        label="Number of albums to show in each list on your profile page (n)",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    track_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of tracks to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )
    album_list_pagination = forms.IntegerField(
        max_value=1000,
        min_value=1,
        label="Number of albums to show in your lists",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-text-field',
            }
        ),
    )

    class Meta:
        model = Profile
        fields = (
            'show_new_posts',
            'show_top_posts',
            'show_new_responses',
            'show_top_responses',
            'n_posts',
            'n_responses',
            'post_list_pagination',
            'response_list_pagination',
            'show_new_articles',
            'show_top_articles',
            'show_new_stories',
            'show_top_stories',
            'show_new_documents',
            'show_top_documents',
            'n_articles',
            'n_stories',
            'n_documents',
            'article_list_pagination',
            'story_list_pagination',
            'document_list_pagination',
            'show_new_visuals',
            'show_top_visuals',
            'show_new_galleries',
            'show_top_galleries',
            'n_visuals',
            'n_galleries',
            'visual_list_pagination',
            'gallery_list_pagination',
            'show_new_tracks',
            'show_top_tracks',
            'show_new_albums',
            'show_top_albums',
            'n_tracks',
            'n_albums',
            'track_list_pagination',
            'album_list_pagination',
        )

class MemberProfileSectionForm(forms.ModelForm):

    is_enabled = forms.BooleanField(
        label="Enabled",
        help_text="""Choose this option if you want this section to appear\
            on your profile page""",
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
            your profile page
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
        model = MemberProfileSection
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
        self.fields['posts'].queryset = Post.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['responses'].queryset = Response.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['articles'].queryset = Article.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['stories'].queryset = Stories.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['documents'].queryset = SupportDocument.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['visuals'].queryset = Visual.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['galleries'].queryset = Gallery.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['tracks'].queryset = Track.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )
        self.fields['albums'].queryset = Album.objects.filter(
            owner=user.pk,
            is_public=True,
        ).order_by(
            '-last_modified',
        )

class InviteLinkCreateForm(forms.ModelForm):

    label = forms.CharField(
        max_length=255,
    )
    note = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-text-field',
            }
        ),
        max_length=1000,
    )

    label.widget.attrs.update({'class': 'form-text-field'})

    class Meta:
        model = InviteLink
        fields = (
            'label',
            'note',
        )
        help_texts = {
            'label': """Label this link for future reference.""",
            'note': """Leave a message for the recipient.""",
        }
