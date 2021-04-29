from django.db import models
from objects.mixins import MetaDataMixin
from crypto.models import CryptoWalletsMixin
from members.mixins import MarshmallowMixin


# Model Mixins 

class AppProfile(models.Model):
    '''
    Modifiable settings for Lookaway apps.
    '''
    class Meta:
        abstract = True

    title = models.CharField(
        max_length=255,
        default="Lookaway CMS"
    )
    show_title = models.BooleanField(default=True)
    meta_description = models.TextField(
        max_length = 155,
        blank=True,
        null=True,
    )
    show_desc = models.BooleanField(default=True)
    text = models.TextField(
        max_length=65535,
        blank=True,
        null=True,
    )
    links = models.ManyToManyField(
        'objects.link',
        blank=True,
    )
    def __str__(self):
        return self.title

class Section(MetaDataMixin):
    '''
    An ordered page section that may contain multimedia objects.
    You must also add a ForeignKey field that points to a model
    which inherits the Doc() mixin below.
    For use with Django models.
    '''
    class Meta:
        abstract = True

    def next_order(self):
        return self.order + 1

    order = models.DecimalField(
        max_digits=8,
        decimal_places=4,
        default=0,
    )
    members_only = models.BooleanField(default=False)
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

class Doc(MetaDataMixin, MarshmallowMixin, CryptoWalletsMixin):
    '''
    A single web page which may contain one or more sections.
    For use with Django models.
    '''

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

# View mixins
class AppPageMixin:

    def get_sets(self, model, n, show_new=True, show_top=True):
        '''
        A method for fetching two model querysets from a Django model.
        Given a model, it will return a list of the newest n items
        whose 'is_public' field is set to true.
        If the number of public models is sufficent, it will
        also return a queryset of at most, the top n items by 'weight'.
        Items that appear in the 'new' queryset will be excluded from
        the 'top' queryset.

        Args:
        instance -  A Django instance with 'is_public', 'publication_date'
                    and 'weight' fields.
        n -         The number of items in each queryset.
        show_new -  If set to False, the 'new_instances' queryset will be empty.
        show_top -  If set to False, the 'top_instances' queryset will be empty.

        Returns:
        new_instances - A queryset of n new public instances of the given instance.
                     Queryset may be less than n if the number of instances
                     is insufficent.
        top_instances - A queryset of the top n public instances by weight
                     of the given instance excluding instances in new_instances.
                     Queryset may be less than n if the number of instances
                     is insufficent.
        '''
        # Initialize variables.
        public_instances = model.objects.filter(is_public=True)
        new_instances = model.objects.none()
        top_instances = model.objects.none()
        # If there are public instances and we want to show the newest n
        if n > 0 and public_instances.count() >= n and show_new:
            # Get the n newest instances.
            new_instances = public_instances.order_by(
                '-publication_date',
            )[:n]
        # If there are public instances and we want to show the top n
        if n > 0 and public_instances.count() >= n and show_top:
            # Get the date of the nth newest instance
            # if there are n or more instances.
            last_new_instance_date = public_instances.order_by(
                '-publication_date',
            )[n-1].publication_date
            # Exclude any instance that appears in the new instances list
            # from the top instance list.
            if show_new:
                top_instances = public_instances.order_by(
                    '-weight',
                ).exclude(
                    publication_date__gte=last_new_instance_date,
                )[:n]
            # Unless new instances aren't being shown, of course
            else:
                print("yep")
                top_instances = public_instances.order_by('-weight')[:n]
        # In the event there are less than n instances,
        # include them in the new model list.
        elif n > 0:
            if show_new:
                new_instances = public_instances.order_by(
                    '-publication_date',
                )
            # Or in the top list if we don't want to show new_models
            elif show_top:
                top_instances = public_instances.order_by(
                    '-weight',
                )
        # Return the querysets
        print({}, ":",  top_instances)
        return new_instances, top_instances

# View mixins
class AppPageMixin:
    '''
    A collection of methods for use with Lookaway app landing views.
    '''

    def get_sets(self, model, n, show_new=True, show_top=True, member=None):
        '''
        A method for fetching two model querysets from a Django model.
        Given a model, it will return a list of the newest n items
        whose 'is_public' field is set to true.
        If the number of public models is sufficent, it will
        also return a queryset of at most, the top n items by 'weight'.
        Items that appear in the 'new' queryset will be excluded from
        the 'top' queryset.
        Useful for assigning context in the 'get_context_data()' method.

        Args:
        instance -  A Django instance with 'is_public', 'publication_date'
                    and 'weight' fields.
        n -         The number of items in each queryset.
        show_new -  If set to False, the 'new_instances' queryset will be empty.
        show_top -  If set to False, the 'top_instances' queryset will be empty.

        Returns:
        new_instances - A queryset of n new public instances of the given instance.
                     Queryset may be less than n if the number of instances
                     is insufficent.
        top_instances - A queryset of the top n public instances by weight
                     of the given instance excluding instances in new_instances.
                     Queryset may be less than n if the number of instances
                     is insufficent.
        '''
        # Initialize variables.
        try:
            public_instances = model.objects.filter(
                is_public=True,
            ).exclude(members_only=True)
            if member != None:
                public_instances = public_instances.all().filter(owner=member)
        except:
            public_instances = model.objects.filter(is_public=True)
            if member != None:
                public_instances = public_instances.all().filter(owner=member)
        new_instances = model.objects.none()
        top_instances = model.objects.none()
        # If there are public instances and we want to show the newest n
        if n > 0 and public_instances.count() >= n and show_new:
            # Get the n newest instances.
            new_instances = public_instances.order_by(
                '-publication_date',
            )[:n]
        # If there are public instances and we want to show the top n
        if n > 0 and public_instances.count() >= n and show_top:
            # Get the date of the nth newest instance
            # if there are n or more instances.
            last_new_instance_date = public_instances.order_by(
                '-publication_date',
            )[n-1].publication_date
            # Exclude any instance that appears in the new instances list
            # from the top instance list.
            if show_new:
                top_instances = public_instances.order_by(
                    '-weight',
                ).exclude(
                    publication_date__gte=last_new_instance_date,
                )[:n]
            # Unless new instances aren't being shown, of course
            else:
                top_instances = public_instances.order_by('-weight')[:n]
        # In the event there are less than n instances,
        # include them in the new model list.
        elif n > 0:
            if show_new:
                new_instances = public_instances.order_by(
                    '-publication_date',
                )
            # Or in the top list if we don't want to show new_models
            elif show_top:
                top_instances = public_instances.order_by(
                    '-weight',
                )
        # Return the querysets
        print({}, ":",  top_instances)
        return new_instances, top_instances

