from django.db import models
from objects.models import MetaDataMixin
from members.mixins import MarshmallowMixin

# Create your models here.

class Section(MetaDataMixin):

    class Meta:
        abstract = True

    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    title = models.CharField(
        max_length=255,
    )
    text = models.TextField(max_length=65535)
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

class Doc(MetaDataMixin, MarshmallowMixin):

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
    )
    slug = models.SlugField(max_length=255, unique=True)
    intro = models.TextField(max_length=65535)
    outro = models.TextField(max_length=65535)
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
    meta_description = models.TextField(
        max_length = 155,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

class Document(Doc):

    pass

class DocumentSection(Section):

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='parent_doc',
    )

class SupportDocument(Doc):

    numbered = models.BooleanField(default=False)
    tip = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
    )
    warning = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
    )

class SupportDocSection(Section):

    support_document = models.ForeignKey(
        SupportDocument,
        on_delete=models.CASCADE,
        related_name='parent_doc',
    ) 
    support_reference = models.ForeignKey(
        SupportDocument,
        on_delete=models.SET_NULL,
        related_name='reference_doc',
        blank=True,
        null=True,
    )

