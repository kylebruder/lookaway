from django.db import models
from django.urls import reverse
from members.mixins import MarshmallowMixin
from objects.mixins import MetaDataMixin
from crypto.models import CryptoWalletsMixin
from lookaway.mixins import AppProfile, Section, Doc

# Create your models here.

class MusicAppProfile(AppProfile, CryptoWalletsMixin):

    title = models.CharField(
        max_length=255,
        default="Music",
    )

    n_tracks = models.PositiveIntegerField(default=3)
    n_albums = models.PositiveIntegerField(default=3)
    track_list_pagination = models.PositiveIntegerField(default=10)
    album_list_pagination = models.PositiveIntegerField(default=10)
    show_new_tracks = models.BooleanField(default=True)
    show_top_tracks = models.BooleanField(default=True)
    show_new_albums = models.BooleanField(default=True)
    show_top_albums = models.BooleanField(default=True)
    logo = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='music_logo'
    )
    banner = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='music_banner'
    )
    bg_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='music_bg_image'
    )
    
class MusicPageSection(Section):

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
    tracks = models.ManyToManyField(
        'music.track',
        blank=True,
    )
    albums = models.ManyToManyField(
        'music.album',
        blank=True,
    )
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Landing Page Section"
        verbose_name_plural = "Landing Page Sections"
        ordering = ['order']

class MusicMetaData(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    members_only = models.BooleanField(default=False)
    artist = models.CharField(max_length=128)
    text = models.TextField(
        max_length=65535,
        blank=True,
    )
    genre = models.CharField(
        max_length=128,
        blank=True,
        )
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    label = models.CharField(
        max_length=128,
        blank=True,
    )
    meta_description = models.TextField(
        max_length = 155,
        blank=True,
        null=True,
    )


class Track(MetaDataMixin, MusicMetaData, MarshmallowMixin, CryptoWalletsMixin):

    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    sound = models.ForeignKey(
        'objects.sound',
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    video = models.ForeignKey(
        'objects.video',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    links = models.ManyToManyField(
        'objects.link',
        blank=True,
    )

    def get_thumbnail(self):
        '''
        Returns a URL that points to a thumbnail image. If it exists,
        the Album cover will used. If there is no Album cover,
        use the owners profile image, otherwise use the site logo.
        '''
        try:
            try:
                return self.image.thumbnail_file.url
            except:
                return self.owner.profile.image.thumbnail_file.url
        except:
            return '/static/icon.webp'

    def get_absolute_url(self):
        return reverse('music:track_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

class Album(MetaDataMixin, MusicMetaData, MarshmallowMixin, CryptoWalletsMixin):

    cover = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tracks = models.ManyToManyField(
        Track,
        blank=True,
    )
    links = models.ManyToManyField(
        'objects.link',
        blank=True,
    )

    def get_thumbnail(self):
        '''
        Returns a URL that points to a thumbnail image. If it exists,
        the Album cover will used. If there is no Album cover,
        use the owners profile image, otherwise use the site logo.
        '''
        try:
            try:
                return self.cover.thumbnail_file.url
            except:
                return self.owner.profile.image.thumbnail_file.url
        except:
            return '/static/icon.webp'

    def get_absolute_url(self):
        return reverse('music:album_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

