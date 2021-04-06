from django.db import models
from crypto.models import CryptoWalletsMixin
from members.mixins import MarshmallowMixin
from lookaway.mixins import AppProfile, Section
from objects.models import MetaDataMixin

# Create your models here.
class PostsAppProfile(AppProfile, CryptoWalletsMixin):

    n_posts = models.PositiveIntegerField(default=25)
    n_responses = models.PositiveIntegerField(default=5)
    post_list_pagination = models.PositiveIntegerField(default=25)
    response_list_pagination = models.PositiveIntegerField(default=6)
    show_new_posts = models.BooleanField(default=True)
    show_top_responses = models.BooleanField(default=True)
    show_new_posts = models.BooleanField(default=True)
    show_top_responses = models.BooleanField(default=True)
    logo = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts_logo'
    )
    banner = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts_banner'
    )
    bg_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts_bg_image'
    )

class PostsPageSection(Section):

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
    posts = models.ManyToManyField(
        'posts.post',
        blank=True,
    )
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Landing Page Section"
        verbose_name_plural = "Landing Page Sections"
        ordering = ['order']

class Post(MetaDataMixin, MarshmallowMixin, CryptoWalletsMixin):

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=255, unique=True)
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
