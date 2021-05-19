from django.db import models
from lookaway.mixins import AppProfile, Section
from crypto.models import CryptoWalletsMixin

# Create your models here.

class HomeAppProfile(AppProfile, CryptoWalletsMixin):

    logo = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='home_logo'
    )
    banner = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='home_banner'
    )
    bg_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='home_bg_image'
    )
    # Navbar
    ## Posts
    nav_show_posts = models.BooleanField(default=True)
    nav_posts_name = models.CharField(
        max_length=64,
        default='Posts',
    )
    nav_posts_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_posts_image',
    )
    ## Documentation
    nav_show_documentation = models.BooleanField(default=True)
    nav_documentation_name = models.CharField(
        max_length=64,
        default='Zine',
    )
    nav_documentation_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_documentation_image',
    )
    ## Art
    nav_show_art = models.BooleanField(default=True)
    nav_art_name = models.CharField(
        max_length=64,
        default='Art',
    )
    nav_art_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_art_image',
    )
    ## Music
    nav_show_music = models.BooleanField(default=True)
    nav_music_name = models.CharField(
        max_length=64,
        default='Music',
    )
    nav_music_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_music_image',
    )
    ## Members
    nav_show_members = models.BooleanField(default=True)
    nav_members_name = models.CharField(
        max_length=64,
        default='Members',
    )
    nav_members_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_members_image',
    )
    ## Objects
    nav_show_objects = models.BooleanField(default=True)
    nav_objects_name = models.CharField(
        max_length=64,
        default='Objects',
    )
    nav_objects_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_objects_image',
    )

    # Posts settings
    n_posts = models.PositiveIntegerField(default=5)
    n_responses = models.PositiveIntegerField(default=5)
    show_new_posts = models.BooleanField(default=True)
    show_top_posts = models.BooleanField(default=True)
    show_new_responses = models.BooleanField(default=False)
    show_top_responses = models.BooleanField(default=False)
    # Documentation settings
    n_articles = models.PositiveIntegerField(default=5)
    n_stories = models.PositiveIntegerField(default=5)
    n_documents = models.PositiveIntegerField(default=5)
    show_new_articles = models.BooleanField(default=True)
    show_top_articles = models.BooleanField(default=True)
    show_new_stories = models.BooleanField(default=True)
    show_top_stories = models.BooleanField(default=True)
    show_new_documents = models.BooleanField(default=True)
    show_top_documents = models.BooleanField(default=True)
    # Art settings
    n_visuals = models.PositiveIntegerField(default=25)
    n_galleries = models.PositiveIntegerField(default=5)
    show_new_visuals = models.BooleanField(default=True)
    show_top_visuals = models.BooleanField(default=True)
    show_new_galleries = models.BooleanField(default=True)
    show_top_galleries = models.BooleanField(default=True)
    # Music settings
    n_tracks = models.PositiveIntegerField(default=5)
    n_albums = models.PositiveIntegerField(default=5)
    show_new_tracks = models.BooleanField(default=True)
    show_top_tracks = models.BooleanField(default=True)
    show_new_albums = models.BooleanField(default=True)
    show_top_albums = models.BooleanField(default=True)
    # Tags
    n_tags = models.PositiveIntegerField(default=50)
    show_tags = models.BooleanField(default=True)
    # Footer
    legal_notice = models.TextField(
        max_length=2048,
        null=True,
        blank=True,
    )
    admin_email = models.EmailField(
        null=True,
        blank=True,
    )
    # CSS
    css_path = models.CharField(
        max_length=2048,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Home App Profile"

    def __str__(self):
        return self.title

class HomePageSection(Section):

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
    responses = models.ManyToManyField(
        'posts.responsepost',
        blank=True,
    )
    articles = models.ManyToManyField(
        'documentation.article',
        blank=True,
    )
    stories = models.ManyToManyField(
        'documentation.story',
        blank=True,
    )
    documents = models.ManyToManyField(
        'documentation.supportdocument',
        blank=True,
    )
    visuals = models.ManyToManyField(
        'art.visual',
        blank=True,
    )
    galleries = models.ManyToManyField(
        'art.gallery',
        blank=True,
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
    members_only = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Home Page Section"
        verbose_name_plural = "Home Page Sections"
        ordering = ['order']

    def __str__(self):
        return self.title
