from django.db import models
from django.urls import reverse
from crypto.models import CryptoWalletsMixin
from lookaway.mixins import AppProfile, Section, Doc

# Create your models here.

class DocumentationAppProfile(AppProfile, CryptoWalletsMixin):

    title = models.CharField(
        max_length=255,
        default="Zine",
    )

    n = models.PositiveIntegerField(default=3)
    list_pagination = models.PositiveIntegerField(default=10)
    show_new_articles = models.BooleanField(default=True)
    show_top_articles = models.BooleanField(default=True)
    show_new_stories = models.BooleanField(default=True)
    show_top_stories = models.BooleanField(default=True)
    show_new_support_documents = models.BooleanField(default=True)
    show_top_support_documents = models.BooleanField(default=True)
    logo = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='documentation_logo'
    )
    banner = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='documentation_banner'
    )
    bg_image = models.ForeignKey(
        'objects.image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='documentation_bg_image'
    )
    
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
        verbose_name = "Landing Page Section"
        verbose_name_plural = "Landing Page Sections"
        ordering = ['order']

class Article(Doc, CryptoWalletsMixin):

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def get_absolute_url(self):
        return reverse('documentation:article_detail', kwargs={'slug': self.slug})

    def get_thumbnail(self):
        '''
        Returns a URL that points to a thumbnail image. If it exists,
        the Article image will used. If there is no Article image,
        use the owners profile image, otherwise use the site logo.
        '''
        try:
            try:
                return self.image.thumbnail_file.url
            except:
                return self.owner.profile.image.thumbnail_file.url
        except:
            return '/static/icon.webp'

    def next_section_order(self):
        '''
        If The Article has Sections, returns a floating point value that 
        equals the highest ordered ArticleSection belonging to the Article
        plus one or else return 1.
        '''
        if ArticleSection.objects.filter(article=self).count() > 0:
            return float(
                ArticleSection.objects.filter(
                    article=self
                ).order_by('order').last().order
            ) + 1
        else:
            return 1

class ArticleSection(Section):

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='parent_article',
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Article Section"
        verbose_name_plural = "Article Sections"


class Story(Doc, CryptoWalletsMixin):

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

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"

    def get_absolute_url(self):
        return reverse('documentation:story_detail', kwargs={'slug': self.slug})

    def get_thumbnail(self):
        '''
        Returns a URL that points to a thumbnail image. If it exists,
        the Story image will used. If there is no Story image,
        use the owners profile image, otherwise use the site logo.
        '''
        try:
            try:
                return self.image.thumbnail_file.url
            except:
                return self.owner.profile.image.thumbnail_file.url
        except:
            return '/static/icon.webp'

    def next_section_order(self):
        '''
        If The Story has Sections, returns a floating point value that 
        equals the highest ordered StorySection belonging to the Story
        plus one or else return 1.
        '''
        if StorySection.objects.filter(story=self).count() > 0:
            return float(
                StorySection.objects.filter(
                    story=self
                ).order_by('order').last().order
            ) + 1
        else:
            return 1

class StorySection(Section):

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='parent_story',
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Story Section"
        verbose_name_plural = "Story Sections"

class SupportDocument(Doc, CryptoWalletsMixin):

    numbered = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Information"
        verbose_name_plural = "Information"

    def get_absolute_url(self):
        return reverse('documentation:support_document_detail', kwargs={'slug': self.slug})

    def get_thumbnail(self):
        '''
        Returns a URL that points to a thumbnail image. If it exists,
        the SupportDocument image will used. If there is no 
        SupportDocument image, use the owners profile image, 
        otherwise use the site logo.
        '''
        try:
            try:
                return self.image.thumbnail_file.url
            except:
                return self.owner.profile.image.thumbnail_file.url
        except:
            return '/static/icon.webp'

    def next_section_order(self):
        '''
        If The SupportDocument has Sections, returns a floating point value that        
        equals the highest ordered SupportDocSection belonging to the SupportDocument
        plus one or else return 1.
        ''' 
        if SupportDocSection.objects.filter(support_document=self).count() > 0:
            return float(
                SupportDocSection.objects.filter(
                    support_document=self
                ).order_by('order').last().order
            ) + 1
        else:
            return 1

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
        verbose_name = "Information Section"
        verbose_name_plural = "Information Sections"
