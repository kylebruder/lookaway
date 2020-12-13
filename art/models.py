from django.db import models
from django.urls import reverse
from members.mixins import MarshmallowMixin
from objects.models import MetaDataMixin

# Create your models here.

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

class Visual(MetaDataMixin, ArtMetaData, MarshmallowMixin):

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

class Gallery(MetaDataMixin, ArtMetaData, MarshmallowMixin):

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
