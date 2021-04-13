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
    nav_posts_name = models.CharField(
        max_length=64,
    )
    nav_posts_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_posts_image',
    )
    nav_documentation_name = models.CharField(
        max_length=64,
    )
    nav_documentation_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_documentation_image',
    )
    nav_art_name = models.CharField(
        max_length=64,
    )
    nav_art_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_art_image',
    )
    nav_music_name = models.CharField(
        max_length=64,
    )
    nav_music_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='nav_music_image',
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
    show_top_visual = models.BooleanField(default=True)
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
