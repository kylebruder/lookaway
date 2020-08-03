from django.db import models
from objects.models import MetaDataMixin
from members.mixins import MarshmallowMixin

# Create your models here.


class SupportDocument(MetaDataMixin, MarshmallowMixin):

    numbered = models.BooleanField(default=False)
    title = models.CharField(
        max_length=64,
    )
    slug = models.SlugField()
    intro = models.TextField(max_length=2048)
    outro = models.TextField(max_length=2048)
    image = models.ForeignKey(
        'objects.image',
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

class Section(MetaDataMixin):

    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(max_length=2048)
    support_document = models.ForeignKey(
        'SupportDocument',
        on_delete=models.CASCADE,
    ) 
    images = models.ManyToManyField(
        'objects.image',
        blank=True,
    )
    sounds = models.ManyToManyField(
        'objects.sound',
        blank=True,
    )
    videos = models.ManyToManyField(
        'objects.video',
        blank=True,
    )
    code = models.ManyToManyField(
        'objects.code',
        blank=True,
    )
    links = models.ManyToManyField(
        'objects.link',
        blank=True,
    )

    def __str__(self):
        return self.title
