from django.db import models
from django.urls import reverse
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

class Doc(MetaDataMixin, MarshmallowMixin):

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
