from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from lookaway.mixins import AppPageMixin
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from objects.models import Tag
from objects.utils import Text
from art.models import Gallery, Visual
from music.models import Album, Track
from documentation.models import Article, Story, SupportDocument
from posts.models import Post, ResponsePost
from .forms import HomeAppProfileForm, HomeAppProfileSettings, HomePageSectionForm
from .models import HomeAppProfile, HomePageSection

# Create your views here.

class HomeAppProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'home.change_homeappprofile'
    model = HomeAppProfile
    form_class = HomeAppProfileForm

    def get_form_kwargs(self):
        kwargs = super(HomeAppProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = HomeAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile".format(profile.title)
        context['sections'] = HomePageSection.objects.all().order_by(
            'order',
        )
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('home:index')

class HomeAppProfileSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView, MemberUpdateMixin):

    permission_required = 'home.change_homeappprofile'
    model = HomeAppProfile
    form_class = HomeAppProfileSettings
    template_name = 'home/homeappprofilesettings_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = HomeAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile settings".format(profile.title)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('home:home_page')

class IndexView(TemplateView, AppPageMixin):

    template_name = 'home/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create a public object tags context
        public_tags = Tag.objects.none()
        tag_models = {Post, Gallery, Visual, Album, Track, Article, SupportDocument}
        for model in tag_models:
            public_tags = public_tags | Tag.get_tags_from_public(model)
        context['tags'] = public_tags.order_by('-weight')[:50]
        # App profile
        profile, created = HomeAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        sections = HomePageSection.objects.filter(
            is_enabled = True,
        ).order_by(
            'order',
        )
        if self.request.user.is_authenticated:
            context['sections'] = sections
        else:
            context['sections'] = sections.exclude(
                members_only=True
            )
        # New and top Post model instances
        context['new_posts'], context['top_posts'] = self.get_sets(
            Post,
            profile.n_posts,
            show_new=profile.show_new_posts,
            show_top=profile.show_top_posts,
        )
        # New and top Response model instances
        context['new_responses'], context['top_responses'] = self.get_sets(
            ResponsePost,
            profile.n_responses,
            show_new=profile.show_new_responses,
            show_top=profile.show_top_responses,
        )
        # New and top Article model instances
        context['new_articles'], context['top_articles'] = self.get_sets(
            Article,
            profile.n_articles,
            show_new=profile.show_new_articles,
            show_top=profile.show_top_articles,
        )
        # New and top Story model instances
        context['new_stories'], context['top_stories'] = self.get_sets(
            Story,
            profile.n_stories,
            show_new=profile.show_new_stories,
            show_top=profile.show_top_stories,
        )
        # New and top Document model instances
        context['new_documents'], context['top_documents'] = self.get_sets(
            SupportDocument,
            profile.n_documents,
            show_new=profile.show_new_documents,
            show_top=profile.show_top_documents,
        )
        # New and top Visual model instances
        context['new_visuals'], context['top_visuals'] = self.get_sets(
            Visual,
            profile.n_visuals,
            show_new=profile.show_new_visuals,
            show_top=profile.show_top_visuals,
        )
        # New and top Gallery model instances
        context['new_galleries'], context['top_galleries'] = self.get_sets(
            Gallery,
            profile.n_galleries,
            show_new=profile.show_new_galleries,
            show_top=profile.show_top_galleries,
        )
        # New and top Track model instances
        context['new_tracks'], context['top_tracks'] = self.get_sets(
            Track,
            profile.n_tracks,
            show_new=profile.show_new_tracks,
            show_top=profile.show_top_tracks,
        )
        # New and top Album model instances
        context['new_albums'], context['top_albums'] = self.get_sets(
            Album,
            profile.n_albums,
            show_new=profile.show_new_albums,
            show_top=profile.show_top_albums,
        )
        # Update AppProfile button
        if self.request.user.has_perm('home.change_homeappprofile'):
            context['show_edit_profile_button'] = True
            context['edit_profile_url'] = reverse(
                'home:home_app_profile_update',
                kwargs={'pk': 1},
            )
        return context

class HomePageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'home.add_homepagesection'
    model = HomePageSection
    form_class = HomePageSectionForm

    def get_form_kwargs(self):
        kwargs = super(HomePageSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['order'] = self.request.GET.get('order')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = HomeAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Page Section"
        context['meta_desc'] = "Add a section to the {} landing page.".format(profile.title)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'home:home_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class HomePageSectionDetailView(LoginRequiredMixin, DetailView):

    model = HomePageSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = HomeAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        return context

class HomePageSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'home.change_homepagesection'
    model = HomePageSection
    form_class = HomePageSectionForm

    def get_form_kwargs(self):
        kwargs = super(HomePageSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = HomeAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this landing page section.".format(self.object.title)
        return context

    def form_valid(self, form):
        # Update last modified date for the Section
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'home:home_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class HomePageSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = 'home.delete_homepagesection'
    model = HomePageSection
    context_object_name = "section"

    def get_success_url(self):
        return reverse(
            'home:home_page',
        )
