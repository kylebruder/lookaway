from django.db import models
from members.mixins import MarshmallowMixin, MemberOwnershipModel
from objects.models import MetaDataMixin

# Create your models here.

class Post(MetaDataMixin, MarshmallowMixin):

    title = models.CharField(max_length=128)
    slug = models.SlugField()
    members_only = models.BooleanField(default=True)
    text = models.TextField(max_length=65535)
    location = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    sound = models.ForeignKey(
        'objects.sound',
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
    code = models.ForeignKey(
        'objects.code',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    link = models.ForeignKey(
        'objects.link',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    re = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    meta_description = models.TextField(
        max_length = 155,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date', '-creation_date']
