from django.db import models
from django.urls import reverse
from crypto.models import CryptoWalletsMixin
from lookaway.mixins import AppProfile, Section, Doc

# Create your models here.

class DocumentationAppProfile(AppProfile, CryptoWalletsMixin):
    pass
    
class DocumentationPageSection(Section):

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
    articles = models.ManyToManyField(
        'documentation.article',
        blank=True,
    )
    stories = models.ManyToManyField(
        'documentation.story',
        blank=True,
    )
    support_documents = models.ManyToManyField(
        'documentation.supportdocument',
        blank=True,
    )
    is_enabled = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

class Article(Doc):

    def get_absolute_url(self):
        return reverse('documentation:article_detail', kwargs={'slug': self.slug})

class ArticleSection(Section):

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='parent_article',
    )

    class Meta:
        ordering = ['order']

class Story(Doc):

    is_fiction = models.BooleanField(default=True)
    author = models.CharField(
        max_length=255,
    )
    translator = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    editor = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    audio_reading = models.ForeignKey(
        'objects.sound',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    original_publisher = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    original_publication_year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse('documentation:story_detail', kwargs={'slug': self.slug})

class StorySection(Section):

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='parent_story',
    )

    class Meta:
        ordering = ['order']

class SupportDocument(Doc):

    numbered = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('documentation:support_document_detail', kwargs={'slug': self.slug})

class SupportDocSection(Section):

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

    class Meta:
        ordering = ['order']
