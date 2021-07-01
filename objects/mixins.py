from django.db import models
from django.utils import timezone

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
    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
    )
    tags = models.ManyToManyField(
        'objects.tag',
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
