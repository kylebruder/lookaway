from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import text
from .models import Member, Profile

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, *args, **kwargs):
    '''
    Create a new Profile when a new member joins the site.
    Add them to a Guest group that allows posting on the site.
    '''
    if created:
        # Give a new member permission to use the Posts app
        # Thank you Bee Keeper!
        # https://gist.github.com/bee-keeper/9857973
        from django.contrib.auth.models import Group
        from django.contrib.auth.models import Permission, ContentType
        post = ContentType.objects.get(app_label='posts', model='post')
        response = ContentType.objects.get(app_label='posts', model='responsepost')
        # Get all permssions for this model
        post_perms = Permission.objects.filter(content_type=post)
        response_perms = Permission.objects.filter(content_type=response)
        # This will override changes made in Admin
        for p in post_perms:
            instance.user_permissions.add(p)
        for p in response_perms:
            instance.user_permissions.add(p)
        # Add slug
        p, c = Profile.objects.get_or_create(member=instance)
        p.slug = text.slugify(instance.username)
        p.save()

