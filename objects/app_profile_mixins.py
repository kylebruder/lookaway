from django.db.models import Q
from home.models import HomeAppProfile
from members.models import Member
from .models import ObjectsAppProfile, Tag
# Model by tag mixin

class ModelListMixin:
    '''
    Context for list views using ObjectsAppProfile.
    '''
    def get_queryset(self, *args, **kwargs):
        return self.model.objects.filter(
            Q(is_public=True) | Q(owner=self.request.user)
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = self.model._meta.verbose_name_plural.capitalize()
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "{} by {} contributors.".format(
            context['app_list_context'],
            profile.title,
        )
        return context

class ModelByTagMixin:
    '''
    Queryset and context for list views that only include instances
    which are tagged with a given tag name which is passed as a slug to
    the view. Also sets the ObjectsAppProfile.
    '''
    def get_queryset(self, *args, **kwargs):
        slug = self.kwargs['slug']
        if self.request.user.is_authenticated:
            return self.model.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            return self.model.objects.filter(
                is_public=True,
                tags__slug__exact=slug,
            ).order_by('-weight')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App Profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        tag = Tag.objects.get(slug=self.kwargs['slug'])
        context['tag'] = tag
        # Home App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        context['app_list_context'] = self.model._meta.verbose_name_plural.capitalize()
        # SEO stuff
        context['meta_title'] = "{} tagged with {} | {}".format(
            self.model._meta.verbose_name_plural,
            tag,
            home.title,
        )
        context['meta_desc'] = """Member contributed {} \
            tagged with {} on {}""".format(
                self.model._meta.verbose_name_plural,
                tag,
                home.title,
            )
        print(self.model._meta.verbose_name_plural)
        return context

class MemberViewMixin:

    def get_queryset(self, *args, **kwargs):
        print('yas')
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return self.model.objects.filter(owner=member)
        else:
            return self.model.objects.filter(
                is_public=True,
                owner=member,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
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
        print(context)
        return context

