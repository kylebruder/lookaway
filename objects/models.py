import hashlib
from django.db import models
from django.urls import reverse
from django.utils import timezone
from members.mixins import MarshmallowMixin


# Create your models here.


### Tags and metadata

## Tag - Key value pairs which can be added to site objects

class Tag(models.Model):

    key = models.CharField(max_length=64)
    value = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    slug = models.SlugField(max_length=255, unique=True)
    marshmallows = models.ManyToManyField('members.marshmallow', blank=True)
    weight = models.FloatField(default=0)
   
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['key', 'value'],
                name='key-value pair',
            )
        ]

    def get_tags_from_public(model):
        '''
        Returns a set of tags related to instances of a given model
        for which "is_public" boolean field True.
        '''
        tags = Tag.objects.none()
        objects = model.objects.filter(is_public=True).prefetch_related('tags')
        for o in objects:
            if o.tags.count() > 0:
                tags = tags.union(o.tags.all())
        return tags

    def __str__(self):
        if self.value:
            return '{}: {}'.format(self.key, self.value)
        else: return '{}'.format(self.key) 

## Metadata Mixin - Common meta data for site objects

class MetaDataMixin(models.Model):
    '''
    A model Mixin that adds meta data and methods which are common to
    all site objects.
    '''

    class Meta:
        abstract = True

    owner = models.ForeignKey(
        'members.member',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,

    )
    creation_date = models.DateTimeField(
        default=timezone.now,
    )
    last_modified = models.DateTimeField(
        default=timezone.now,
    )
    is_public = models.BooleanField(
        default=False,
    )
    publication_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
    )

    def publish(self, instance, member):
        '''
        If the instance passed belongs to the user then set
        it to public and set the publication date to now.

        Arguments:
        instance - Any instance of a DB model instance that uses MetaDataMixin
        user - Pass request.user when calling from a view

        Returns:
        True - If the instance belongs to the user
        False - If the above condition is not met
        '''
        if instance.owner == member:
            instance.is_public = True
            print("publishing {} on {}".format(instance, timezone.now()))
            instance.publication_date = timezone.now()
            instance.save()
            return True
        else:
            return False


### Site Objects

## Image - Digital visual media uploaded by a Member

# User specific paths for image uploads
def member_image_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/images/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

def member_thumbnail_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/thumbnails/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

class Image(MetaDataMixin, MarshmallowMixin):

    image_file = models.ImageField(
        upload_to=member_image_dir,
        max_length=255,
    )
    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    credit = models.CharField(
        max_length=256,
        blank = True,
        null = True,
    )
    thumbnail_file = models.ImageField(
        upload_to=member_thumbnail_dir,
        max_length=255,
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('objects:image_detail', kwargs={'pk': self.pk})
   
    class Meta:
        ordering = ['-creation_date']

def promote_image(request, pk):
    member = get_object_or_404(Member, pk=request.user.pk)
    instance = get_object_or_404(Image, pk=pk)
    successful, image, weight = member.allocate_weight(instance, Image)
    if successful:
        messages.add_message(
            request, messages.INFO,
            'You gave a marshmallow to {} weighing {}'.format(
                image,
                round(weight, 2)
            )
       )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'You failed to give a marshmallow to {}'.format(image)
        )
    return HttpResponseRedirect(reverse('objects:image_detail', kwargs={'pk': instance.pk}))

## Sound - Digital audio media uploaded by a Member

# User specific path for audio uploads
def member_sound_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/sounds/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

class Sound(MetaDataMixin, MarshmallowMixin):

    sound_file = models.FileField(
        upload_to=member_sound_dir,
        max_length=256,
    )
    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    credit = models.CharField(
        max_length=256,
        blank = True,
        null = True,
    )

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('objects:sound_detail', kwargs={'pk': self.pk})

## Video - Digital video media uploaded by a Member

# User specific path for audio uploads
def member_video_dir(instance, filename):
    try:
        owner = instance.owner.id
    except:
        owner = 0
    return instance.creation_date.strftime(
        'member_{0}/videos/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )


class Video(MetaDataMixin, MarshmallowMixin):

    video_file = models.FileField(
        upload_to=member_video_dir,
        max_length=256,
    )
    title = models.CharField(
        max_length=64,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    credit = models.CharField(
        max_length=256,
        blank = True,
        null = True,
    )

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('objects:video_detail', kwargs={'pk': self.pk}) 

## Code - Used to hold examples of code to be displayed on a page inside <pre> tags
class Code(MetaDataMixin, MarshmallowMixin):

    title = models.CharField(
        max_length=256,
    )
    text = models.TextField(
        max_length=1024,
        blank = True,
        null = True,
    )
    code = models.TextField(
        max_length=65535,
    )
    language = models.CharField(
        max_length=64,
    )
    language_version = models.CharField(
        max_length=64,
    )
    file_path = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    source = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    source_url = models.URLField(
        max_length=256,
        blank=True,
        null=True,
    )
    md5 = models.CharField(
        max_length=32,
    )

    class Meta:
        ordering = ['title', 'language',]

    def __str__(self):
        return '{} - {} {}'.format(self.title, self.language, self.language_version,)

    def get_absolute_url(self):
        return reverse('objects:code_detail', kwargs={'pk': self.pk,})

    def get_md5(string):
        '''
        Given a string, returns a MD5 hash digest
        '''
        md5 = hashlib.md5(string.encode())
        digest = md5.hexdigest()
        return digest

## Link - External URL for online resources outside of the site domain

class Link(MetaDataMixin, MarshmallowMixin):

    title = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    url = models.URLField(
        max_length=256,
    )
    favicon_href = models.URLField(
        max_length=256,
        blank=True,
        null=True,
    )
    text = models.TextField(
        max_length=512,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['-creation_date']
        
    def __str__(self):
        if self.title:
            return self.title
        else:
            if len(self.url) > 64:
                return self.url[0:64] + "..."
            else:
                return self.url

    def get_absolute_url(self):
        return reverse('objects:link_detail', kwargs={'pk': self.pk})
