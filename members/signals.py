from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import text
from .models import Member, Profile

@receiver(post_save, sender=Member)
def create_member_profile(sender, instance, created, *args, **kwargs):
    '''
    Create a new Profile when a new member joins the site
    '''
    if created:
        p, c = Profile.objects.get_or_create(member=instance)
        p.slug = text.slugify(instance.username)
        p.save()

