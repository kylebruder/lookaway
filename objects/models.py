from django.db import models
from django.utils import timezone
from members.mixins import MemberOwnershipModel, MarshmallowMixin

# Create your models here.


### Tags and metadata

## Tag - Key value pairs which can be added to site objects

class Tag(models.Model):

    key = models.CharField(max_length=64, unique=True)
    value = models.CharField(max_length=64)
   
    class Meta:
        ordering = ['key', 'value']

    def __str__(self):
        return '{}: {}'.format(key, value)

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
        'media/member_{0}/images/%Y/%m/%d/{1}'.format(
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
        'media/member_{0}/thumbnails/%Y/%m/%d/{1}'.format(
            owner,
            filename
        )
    )

class Image(MetaDataMixin, MemberOwnershipModel, MarshmallowMixin):

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
        return reverse('images:image_detail', kwargs={'pk': self.pk})
   
    class Meta:
        ordering = ['-creation_date']

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

class Sound(MetaDataMixin, MemberOwnershipModel, MarshmallowMixin):

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

## Code - Used to hold examples of code to be displayed on a page inside <pre> tags

class Code(MetaDataMixin, MemberOwnershipModel, MarshmallowMixin):

    title = models.CharField(
        max_length=256,
    )
    code = models.TextField(
        max_length=4092,
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
        null = True,
    )
    source = models.CharField(
        max_length=64,
        blank=True,
        null = True,
    )

    class Meta:
        ordering = ['title', 'language',]

    def __str__(self):
        return '{0} - {1} {2}'.format(title, language, language_version,)

    def get_absolute_url(self):
        return reverse('objects:code_block_detail', kwargs={'pk': self.pk,})

## Link - External URL for online resources outside of the site domain

class Link(MetaDataMixin, MemberOwnershipModel, MarshmallowMixin):

    title = models.CharField(
        max_length=256,
    )
    url = models.URLField(
        max_length=256,
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
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
        return self.title

    def get_absolute_url(self):
        return reverse('objects:link_detail', kwargs={'pk': self.pk})
