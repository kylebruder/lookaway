from django.db import models
from members.mixins import MarshmallowMixin, MemberOwnershipModel
from objects.models import MetaDataMixin

# Create your models here.

class MusicMetaData(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(max_length=255)
    members_only = models.BooleanField(default=True)
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


class Track(MetaDataMixin, MusicMetaData, MarshmallowMixin):

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

    def __str__(self):
        return self.title

class Album(MetaDataMixin, MusicMetaData, MarshmallowMixin):

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

    def __str__(self):
        return self.title

