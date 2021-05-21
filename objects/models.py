import hashlib
from itertools import chain
from django.db import models
from django.urls import reverse
from django.utils import timezone
from lookaway.mixins import AppProfile, Section
from crypto.models import CryptoWalletsMixin
from members.mixins import MarshmallowMixin
from .mixins import MetaDataMixin


# Create your models here.


### Tags and metadata

## Tag - Key value pairs which can be added to site objects

class ObjectsAppProfile(AppProfile, CryptoWalletsMixin):

    title = models.CharField(
        max_length=255,
        default="Multimedia",
    )
    show_images = models.BooleanField(default=True)
    show_sounds = models.BooleanField(default=True)
    show_videos = models.BooleanField(default=True)
    show_codes = models.BooleanField(default=True)
    show_links = models.BooleanField(default=True)
    n_images = models.PositiveIntegerField(default=18)
    n_sounds = models.PositiveIntegerField(default=5)
    n_videos = models.PositiveIntegerField(default=5)
    n_codes = models.PositiveIntegerField(default=5)
    n_links = models.PositiveIntegerField(default=5)
    images_list_pagination = models.PositiveIntegerField(default=25)
    sounds_list_pagination = models.PositiveIntegerField(default=10)
    videos_list_pagination = models.PositiveIntegerField(default=10)
    codes_list_pagination = models.PositiveIntegerField(default=10)
    links_list_pagination = models.PositiveIntegerField(default=10)
    logo = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='objects_logo'
    )
    banner = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='objects_banner'
    )
    bg_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='objects_bg_image'
    )

    # Media transcoding options
    ## Path ffmpeg binary (you must have this installed)
    ffmpeg_path = models.CharField(
        max_length=64,
        default="/usr/bin/ffmpeg"
    )

    ## Image dimensions in pixels
    image_max_height = models.PositiveIntegerField(default=2500)
    image_max_width = models.PositiveIntegerField(default=2500)
    thumbnail_max_height = models.PositiveIntegerField(default=250)
    thumbnail_max_width = models.PositiveIntegerField(default=250)

    ## Media formats
    image_format = models.CharField(
        max_length=4,
    )
    sound_format = models.CharField(
        max_length=4,
    )
    video_format = models.CharField(
        max_length=4,
    )
    ## Bitrate in Kbps
    sound_bitrate = models.PositiveIntegerField(default=320)
    video_bitrate = models.PositiveIntegerField(default=2048)
    ## Lower value is better quality for these settings
    sound_crf = models.PositiveIntegerField(default=10)
    sound_qmin = models.PositiveIntegerField(default=0)
    sound_qmax = models.PositiveIntegerField(default=51)
    video_crf = models.PositiveIntegerField(default=10)
    video_qmin = models.PositiveIntegerField(default=0)
    video_qmax = models.PositiveIntegerField(default=51)

    class Meta:
        verbose_name = "App Profile"

    def __str__(self):
        return self.title

class ObjectsPageSection(Section):

    info = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
    )
    alert = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
    )
    images = models.ManyToManyField(
        'objects.image',
        blank=True,
        related_name='section_images'
    )
    sounds = models.ManyToManyField(
        'objects.sound',
        blank=True,
        related_name='section_sounds'
    )
    videos = models.ManyToManyField(
        'objects.video',
        blank=True,
        related_name='section_videos'
    )
    codes = models.ManyToManyField(
        'objects.code',
        blank=True,
        related_name='section_codes'
    )
    links = models.ManyToManyField(
        'objects.link',
        blank=True,
        related_name='section_links'
    )
    is_enabled = models.BooleanField(default=False)
    members_only = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Landing Page Section"
        verbose_name_plural = "Landing Page Sections"
        ordering = ['order']

    def __str__(self):
        return self.title

class Tag(models.Model):

    key = models.CharField(max_length=64)
    value = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    marshmallows = models.ManyToManyField('members.marshmallow', blank=True)
    weight = models.FloatField(default=0)
   
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['key', 'value'],
                name='key-value pair',
            )
        ]

    def get_tags_from_public(model):
        '''
        Returns a queryset of tags related to instances of a given model
        for which "is_public" boolean field True.
        '''
        tags = Tag.objects.none()
        objects = model.objects.filter(is_public=True).prefetch_related('tags')
        for o in objects:
            if o.tags.count() > 0:
                # Merge tags into queryset
                tags = tags | o.tags.all()
        return tags.distinct()

    def __str__(self):
        if self.value:
            return '{}: {}'.format(self.key, self.value)
        else: return '{}'.format(self.key) 

### Site Objects

## Image - Digital visual media uploaded by a Member

# User specific paths for image uploads
def member_image_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/images/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

def member_thumbnail_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/thumbnails/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

class Image(MetaDataMixin, MarshmallowMixin):

    image_file = models.ImageField(
        upload_to=member_image_dir,
        max_length=255,
    )
    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    credit = models.CharField(
        max_length=256,
        blank = True,
        null = True,
    )
    thumbnail_file = models.ImageField(
        upload_to=member_thumbnail_dir,
        max_length=255,
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('objects:image_detail', kwargs={'pk': self.pk})
   
    class Meta:
        ordering = ['-creation_date']

def promote_image(request, pk):
    member = get_object_or_404(Member, pk=request.user.pk)
    instance = get_object_or_404(Image, pk=pk)
    successful, image, weight = member.allocate_weight(instance, Image)
    if successful:
        messages.add_message(
            request, messages.INFO,
            'You gave a marshmallow to {} weighing {}'.format(
                image,
                round(weight, 2)
            )
       )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'You failed to give a marshmallow to {}'.format(image)
        )
    return HttpResponseRedirect(reverse('objects:image_detail', kwargs={'pk': instance.pk}))

## Sound - Digital audio media uploaded by a Member

# User specific path for audio uploads
def member_sound_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/sounds/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

class Sound(MetaDataMixin, MarshmallowMixin):

    sound_file = models.FileField(
        upload_to=member_sound_dir,
        max_length=256,
    )
    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    credit = models.CharField(
        max_length=256,
        blank = True,
        null = True,
    )

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('objects:sound_detail', kwargs={'pk': self.pk})

## Video - Digital video media uploaded by a Member

# User specific path for audio uploads
def member_video_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/videos/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )


class Video(MetaDataMixin, MarshmallowMixin):

    video_file = models.FileField(
        upload_to=member_video_dir,
        max_length=256,
    )
    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    credit = models.CharField(
        max_length=256,
        blank = True,
        null = True,
    )

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('objects:video_detail', kwargs={'pk': self.pk}) 

## Code - Used to hold examples of code to be displayed on a page inside <pre> tags
class Code(MetaDataMixin, MarshmallowMixin):

    title = models.CharField(
        max_length=256,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    code = models.TextField(
        max_length=65535,
    )
    language = models.CharField(
        max_length=64,
    )
    language_version = models.CharField(
        max_length=64,
    )
    file_path = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    source = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    source_url = models.URLField(
        max_length=256,
        blank=True,
        null=True,
    )
    md5 = models.CharField(
        max_length=32,
    )

    class Meta:
        ordering = ['title', 'language',]

    def __str__(self):
        return '{} - {} {}'.format(self.title, self.language, self.language_version,)

    def get_absolute_url(self):
        return reverse('objects:code_detail', kwargs={'pk': self.pk,})

    def get_md5(string):
        '''
        Given a string, returns a MD5 hash digest
        '''
        md5 = hashlib.md5(string.encode())
        digest = md5.hexdigest()
        return digest

## Link - External URL for online resources outside of the site domain

class Link(MetaDataMixin, MarshmallowMixin):

    title = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    url = models.URLField(
        max_length=256,
    )
    favicon_href = models.URLField(
        max_length=256,
        blank=True,
        null=True,
    )
    text = models.TextField(
        max_length=512,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-creation_date']
        
    def __str__(self):
        if self.title:
            return self.title
        else:
            if len(self.url) > 64:
                return self.url[0:64] + "..."
            else:
                return self.url

    def get_domain(self):
        return urlparse(self.url).hostname

    def get_absolute_url(self):
        return reverse('objects:link_detail', kwargs={'pk': self.pk})
