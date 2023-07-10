from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import text
from .models import Member, Profile

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, *args, **kwargs):
    '''
    Create default groups.
    Create a new Profile when a new member joins the site.
    Give them permission to make posts and responses.
    '''
    if created:
        from django.contrib.auth.models import Group
        from django.contrib.auth.models import Permission, ContentType
        from itertools import chain

        def get_multiple_model_perms(app, models):
            '''
            Get a queryset of permissions related to multiple content types.
            Args:
            app - The app name in string form
            models - a list of model names in string form

            Returns a queryset of all specified permission objects.

            Thank you Bee Keeper!
            https://gist.github.com/bee-keeper/9857973
            '''
            perms = Permission.objects.none()
            for m in models:
                content_type = ContentType.objects.get(app_label=app, model=m)
                perms = perms | Permission.objects.filter(content_type=content_type)
            return perms

        def get_or_create_group(name, perms):
            '''
            Programatically create a group.
            Args:
            name - The name of the group in string form
            perms - A queryset of permission objects

            If a group with the given name already exists,
            nothing will happen
            '''
            group, new = Group.objects.get_or_create(name=name)
            for p in perms:
                group.permissions.add(p)

        # Default groups
        ## Members
        get_or_create_group(
            "Members",
            get_multiple_model_perms(
                'posts',
                ['post','responsepost',]
            )
        )    
        get_or_create_group(
            "Members",
            get_multiple_model_perms(
                'members',
                ['memberprofilesection',]
            )
        )    
        ## Contributors
        get_or_create_group(
            "Contributors",
            get_multiple_model_perms(
                'objects',
                ['image','sound', 'video', 'code', 'link',]
            )
        )    
        ## Writers
        get_or_create_group(
            "Writers",
            get_multiple_model_perms(
                'documentation', [
                    'article',
                    'articlesection',
                    'story',
                    'storysection',
                    'supportdocument',
                    'supportdocsection',
                ]
            ),
        )    
        ## Artists
        get_or_create_group(
            "Artists",
            get_multiple_model_perms(
                'art',
                ['visual','gallery',]
            ),
        )    
        ## Musicians
        get_or_create_group(
            "Musicians",
            get_multiple_model_perms(
                'music',
                ['track','album',]
            ),
        )    
        # Add them to the members group
        members_group = Group.objects.get(name="Members")
        members_group.user_set.add(instance)
        
        # Add slug
        p, c = Profile.objects.get_or_create(member=instance)
        p.slug = text.slugify(instance.username)
        p.save()

