from django.db import models
from objects.models import MetaDataMixin
from crypto.models import CryptoWalletsMixin
from members.mixins import MarshmallowMixin


# Model Mixins 

class AppProfile(models.Model):
    '''
    Modifiable settings for Lookaway apps.
    '''
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
        default="Lookaway CMS"
    )
    show_title = models.BooleanField(default=True)
    meta_description = models.TextField(
        max_length = 155,
        blank=True,
        null=True,
    )
    show_desc = models.BooleanField(default=True)
    text = models.TextField(
        max_length=65535,
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
    '''
    An ordered page section that may contain multimedia objects.
    You must also add a ForeignKey field that points to a model
    which inherits the Doc() mixin below.
    For use with Django models.
    '''
    class Meta:
        abstract = True

    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    hide_title = models.BooleanField(default=False)
    title = models.CharField(
        max_length=255,
    )
    text = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
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

class Doc(MetaDataMixin, MarshmallowMixin, CryptoWalletsMixin):
    '''
    A single web page which may contain one or more sections.
    For use with Django models.
    '''

    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
    )
    slug = models.SlugField(max_length=255, unique=True)
    intro = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
        )
    outro = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
)
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

