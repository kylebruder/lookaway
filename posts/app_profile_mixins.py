from django.db.models import Q
from home.models import HomeAppProfile
from members.models import Member
from objects.models import Tag
from .models import PostsAppProfile
# Model by tag mixin

class NewModelListMixin:
    '''
    Queryset and context for new list views using PostsAppProfile.
    '''
    def get_queryset(self, *args, **kwargs):
        context = super().get_queryset(**kwargs)
        if self.request.user.is_authenticated:
            return self.model.objects.filter(
                is_public=True,
            ).order_by('-publication_date', '-creation_date')
        else:
            return self.model.objects.filter(
                Q(is_public=True) & Q(members_only=False)
            ).order_by('-publication_date', '-creation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New " + self.model._meta.verbose_name_plural.capitalize()
        # SEO stuff
        context['meta_title'] = "New {} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "New {} by {} contributors.".format(
            context['app_list_context'],
            profile.title,
        )
        return context

class TopModelListMixin:
    '''
    Queryset and context for top list views using PostsAppProfile.
    '''
    def get_queryset(self, *args, **kwargs):
        context = super().get_queryset(**kwargs)
        if self.request.user.is_authenticated:
            return self.model.objects.filter(
                is_public=True,
            ).order_by('-weight')
        else:
            return self.model.objects.filter(
                Q(is_public=True) & Q(members_only=False)
            ).order_by('-weight')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top " + self.model._meta.verbose_name_plural.capitalize()
        # SEO stuff
        context['meta_title'] = "Top {} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "Top {} by {} contributors.".format(
            context['app_list_context'],
            profile.title,
        )
        return context

class StudioListMixin:
    '''
    Queryset and context for studio list views that show every instance of a
    given model which is owned by the requester. Sorts by most recently modified. 
    Also sets the PostsAppProfile.
    '''
    def get_queryset(self, *args, **kwargs):
        member = self.request.user
        return self.model.objects.filter(owner=member).order_by(
                '-last_modified',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "All " + self.model._meta.verbose_name_plural.capitalize()
        context['meta_title'] = "Your {}".format(
            self.model._meta.verbose_name_plural.capitalize(),
            )
        context['meta_desc'] = "Your {}.".format(
            self.model._meta.verbose_name_plural.capitalize(),
        )
        context['member'] = member
        return context

class ModelByMemberMixin:
    '''
    Queryset and context for list views that only include instances
    which are owned by a specific member who's username is passed as a slug to
    the view. Also sets the PostsAppProfile.
    '''
    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return self.model.objects.filter(
            is_public=True,
            owner=member,
        ).order_by('-weight')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = self.model._meta.verbose_name_plural.capitalize()
        context['meta_title'] = "{} by {} | {}".format(
            self.model._meta.verbose_name_plural.capitalize(),
            member,
            profile.title,
            )
        context['meta_desc'] = "{} contributed by {} on {}.".format(
            self.model._meta.verbose_name_plural.capitalize(),
            member,
            profile.title,
        )
        return context
