from django.db import models
from django.urls import reverse
from members.mixins import MarshmallowMixin
from objects.mixins import MetaDataMixin
from crypto.models import CryptoWalletsMixin
from lookaway.mixins import AppProfile, Section, Doc

# Create your models here.

class ArtAppProfile(AppProfile, CryptoWalletsMixin):

    n_visuals = models.PositiveIntegerField(default=25)
    n_galleries = models.PositiveIntegerField(default=5)
    visual_list_pagination = models.PositiveIntegerField(default=25)
    gallery_list_pagination = models.PositiveIntegerField(default=6)
    show_new_visuals = models.BooleanField(default=True)
    show_top_visuals = models.BooleanField(default=True)
    show_new_galleries= models.BooleanField(default=True)
    show_top_galleries = models.BooleanField(default=True)
    logo = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='art_logo'
    )
    banner = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='art_banner'
    )
    bg_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='art_bg_image'
    )
    
class ArtPageSection(Section):

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
    visuals = models.ManyToManyField(
        'art.visual',
        blank=True,
    )
    galleries = models.ManyToManyField(
        'art.gallery',
        blank=True,
    )
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Landing Page Section"
        verbose_name_plural = "Landing Page Sections"
        ordering = ['order']

class ArtMetaData(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    artist = models.CharField(max_length=128)
    text = models.TextField(
        max_length=65535,
        blank=True,
    )
    meta_description = models.TextField(
        max_length = 155,
        blank=True,
        null=True,
    )

class Visual(MetaDataMixin, ArtMetaData, MarshmallowMixin, CryptoWalletsMixin):

    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    image = models.ForeignKey(
        'objects.image',
        on_delete=models.CASCADE,
    )
    video = models.ForeignKey(
        'objects.video',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )
    medium = models.CharField(
        max_length=1028,
        blank=True,
    )
    dimensions = models.CharField(
        max_length=1028,
        blank=True,
    )
    credits = models.CharField(
        max_length=1028,
        blank=True,
    )
    links = models.ManyToManyField(
        'objects.link',
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('art:visual_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title

class Gallery(MetaDataMixin, ArtMetaData, MarshmallowMixin, CryptoWalletsMixin):

    visuals = models.ManyToManyField(
        Visual,
        blank=True,
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
    location = models.CharField(
        max_length=128,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('art:gallery_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
