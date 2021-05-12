from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils import timezone, text
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from lookaway.mixins import AppPageMixin
from objects.utils import Text
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from posts.models import ResponsePost
from .forms import ArtAppProfileForm, ArtPageSectionForm, GalleryForm, VisualForm
from .models import ArtAppProfile, ArtPageSection, Gallery, Visual
# Create your views here.

# Documentation App Profile Form
class ArtAppProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'art.change_artappprofile'
    model = ArtAppProfile
    form_class = ArtAppProfileForm

    def get_form_kwargs(self):
        kwargs = super(ArtAppProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile settings".format(profile.title)
        context['sections'] = ArtPageSection.objects.all().order_by(
            'order',
        )
        # Add art page section button
        if self.request.user.has_perm('art.add_artpagesection'):
            context['show_art_page_section_add_button'] = True
            context['art_page_section_add_button'] = { 
                'url': reverse(
                    'art:art_page_section_create',
                ),
            }
        # Edit art page section button
        if self.request.user.has_perm('art.change_artpagesection'):
            context['show_art_page_section_edit_button'] = True
        # Delete art page section button
        if self.request.user.has_perm('art.delete_artpagesection'):
            context['show_art_page_section_delete_button'] = True
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('art:art_page')

class ArtPageView(TemplateView, AppPageMixin):

    template_name = 'art/art_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        sections = ArtPageSection.objects.filter(
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
        # Galleries
        context['new_galleries'], context['top_galleries'] = self.get_sets(
            Gallery,
            profile.n_galleries,
            show_new=profile.show_new_galleries,
            show_top=profile.show_top_galleries,
        )
        # Visuals
        context['new_visuals'], context['top_visuals'] = self.get_sets(
            Visual,
            profile.n_visuals,
            show_new=profile.show_new_visuals,
            show_top=profile.show_top_visuals,
        )
        # Create Visual button
        if self.request.user.has_perm('art.add_post'):
            context['show_visual_add_button'] = True
            context['visual_add_button'] = {
                'url': reverse('art:visual_create'),
                'text': "+Visual",
            }
        # Create Gallery button
        if self.request.user.has_perm('art.add_gallery'):
            context['show_gallery_add_button'] = True
            context['gallery_add_button'] = {
                'url': reverse('art:gallery_create'),
                'text': "+Gallery",
            }
        # Update AppProfile button
        if self.request.user.has_perm('art.change_artappprofile'):
            context['show_profile_edit_button'] = True
            context['profile_edit_button'] = {
                'url': reverse('art:art_app_profile_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit App"
            }
        # Add art page section button
        if self.request.user.has_perm('art.add_artpagesection'):
            context['show_art_page_section_add_button'] = True
            context['art_page_section_add_button'] = { 
                'url': reverse(
                    'art:art_page_section_create',
                ),
            }
        # Edit art page section button
        if self.request.user.has_perm('art.change_artpagesection'):
            context['show_art_page_section_edit_button'] = True
        # Delete art page section button
        if self.request.user.has_perm('art.delete_artpagesection'):
            context['show_art_page_section_delete_button'] = True
        return context

# Art Page Section Views
class ArtPageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = 'art.add_artpagesection'
    model = ArtPageSection
    form_class = ArtPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(ArtPageSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Page Section"
        context['meta_desc'] = "Add a section to the {} landing page.".format(profile.title)
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
                'art:art_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class ArtPageSectionDetailView(LoginRequiredMixin, DetailView):

    model = ArtPageSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        # Add art page section button
        if self.request.user.has_perm('art.add_artpagesection'):
            context['show_art_page_section_add_button'] = True
            context['art_page_section_add_button'] = {
                'url': reverse(
                    'art:art_page_section_create',
                ),
            }
        # Edit art page section button
        if self.request.user.has_perm('art.change_artpagesection'):
            context['show_art_page_section_edit_button'] = True
        # Delete art page section button
        if self.request.user.has_perm('art.delete_artpagesection'):
            context['show_art_page_section_delete_button'] = True
        return context

class ArtPageSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'art.change_artpagesection'
    model = ArtPageSection
    form_class = ArtPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(ArtPageSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
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
                'art:art_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class ArtPageSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = 'art.delete_artpagesection'
    model = ArtPageSection
    context_object_name = "section"

    def get_success_url(self):
        return reverse(
            'art:art_page',
        )

# Gallery Views
class GalleryCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'art.add_gallery'
    model = Gallery
    form_class = GalleryForm

    def get_form_kwargs(self):
        kwargs = super(GalleryCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Gallery"
        context['meta_desc'] = """Submit an Gallery you wish to publish. \
            First, create some visuals then choose which Visuals will appear \
            in the Gallery in the form below."""
        context['profile'] = profile
        return context

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = Text.slugify_unique(self.model, form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'art:gallery_detail',
                kwargs={'slug': self.object.slug},
            )

class GalleryListView(ListView):

    model = Gallery
    paginate_by = ArtAppProfile.objects.get_or_create(pk=1)[0].gallery_list_pagination
    context_object_name = 'galleries'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Gallery.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Gallery.objects.filter(
                is_public=True,
            ).order_by(
                '-publication_date',
            )
        # Create button
        if self.request.user.has_perm('art.add_gallery'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'art:gallery_create',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Galleries"
        # SEO stuff
        context['meta_title'] = "New Galleries | {}".format(
            profile.title,
        )
        context['meta_desc'] = "The latest galleries curated by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('art.add_gallery'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'art:gallery_create',
            )
        return context

class TopGalleryListView(ListView):

    model = Gallery
    paginate_by = ArtAppProfile.objects.get_or_create(pk=1)[0].gallery_list_pagination
    context_object_name = 'galleries'

    def get_queryset(self, *args, **kwargs):
        return Gallery.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Galleries"
        # SEO stuff
        context['meta_title'] = "Top Galleries | {}".format(
            profile.title,
        )
        context['meta_desc'] = "Amazing galleries curated by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('art.add_gallery'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'art:gallery_create',
            )
        return context

class GalleryDetailView(DetailView):

    model = Gallery
    context_object_name = 'gallery'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            # Post Actions
            if self.object.owner.pk == member.pk:
                if not self.object.is_public:
                    context['show_publish_button'] = True
                    context['publish_button'] = {
                        'url': reverse(
                            'art:publish_gallery',
                            kwargs={
                                'pk': self.object.pk,
                            },
                        )
                    }
                context['show_edit_button'] = True
                context['edit_button'] = {
                     'url': reverse(
                        'art:gallery_update',
                        kwargs={
                            'slug': self.object.slug,
                        },
                    )
                }
                context['show_delete_button'] = True
                context['delete_button'] = {
                     'url': reverse(
                        'art:gallery_delete',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    )
                }
            # Marshmallow button
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
                context['marshmallow_button'] = {
                    'url': reverse(
                        'art:gallery_marshmallow',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    ),
                }
            # Response button
            if self.request.user.has_perms('posts:add_response'):
                context['can_respond'] = True
                context['response_button'] = {
                    'url': reverse(
                        'posts:response_post_create',
                        kwargs={
                            'model': "gallery",
                            'pk': self.object.pk,
                            'members_only': False
                        },
                    ),
                }
            # Get the posts that are a response to this gallery
            context['responses'] = ResponsePost.objects.filter(
                gallery=self.object,
                is_public=True,
            ).order_by('weight', '-publication_date')[:5]
        else:
            context['responses'] = ResponsePost.objects.filter(
                gallery=self.object,
                is_public=True,
                members_only=False,
            ).order_by('weight', '-publication_date')[:5]
        return context

class MemberGalleryView(ListView):

    model = Gallery
    paginate_by = ArtAppProfile.objects.get_or_create(pk=1)[0].gallery_list_pagination
    context_object_name = 'galleries'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return Gallery.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else:
            return Gallery.objects.filter(
                owner=member,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Galleries"
        context['meta_title'] = "Galleries by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Galleries curated by {} for {}.".format(
            member,
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('art.add_gallery'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'art:gallery_create',
            )
        context['member'] = member
        return context

class GalleryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'art.change_gallery'
    model = Gallery
    form_class = GalleryForm

    def get_form_kwargs(self):
        kwargs = super(GalleryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this gallery.".format(self.object.title)
        return context

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'art:gallery_detail',
                kwargs={'slug': self.object.slug},
            )

class GalleryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'art.delete_gallery'
    model = Gallery

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_gallery_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Gallery, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Gallery)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Gallery.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('art:top_galleries'))

def publish_gallery_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Gallery, pk=pk)
    if request.method == 'GET':
        template = loader.get_template('publish.html')
        context = {'object': instance}
        return render(request, 'publish.html', context)
    elif request.method == 'POST':
        successful = instance.publish(instance, member)
        if successful:
            messages.add_message(
                request,
                messages.INFO,
                '{} has been published'.format(
                    instance,
                )
            )
            return HttpResponseRedirect(
                reverse(
                    'art:gallery_detail',
                    kwargs={
                        'slug': instance.slug,
                    }
                )
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                '{} could not be published'.format(
                    instance,
                )
            )
            return HttpResponseRedirect(
                reverse(
                'art:gallery_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# Visual Views

class VisualCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'art.add_visual'
    model = Visual
    form_class = VisualForm

    def get_form_kwargs(self):
        kwargs = super(VisualCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if 'image' in self.request.GET:
            kwargs['image'] = self.request.GET.get('image')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Visual"
        context['meta_desc'] = """Submit a Visual you wish to publish. \
            First upload an image file then choose it in the form below."""
        context['profile'] = profile
        return context

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = Text.slugify_unique(self.model, form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy(
                'art:visual_detail',
                kwargs={'slug': self.object.slug},
            )

class VisualListView(ListView):

    model = Visual
    paginate_by = ArtAppProfile.objects.get_or_create(pk=1)[0].visual_list_pagination
    context_object_name = 'visuals'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Visual.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Visual.objects.filter(
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Visuals"
        # SEO stuff
        context['meta_title'] = "New Visuals | {}".format(
            profile.title,
        )
        context['meta_desc'] = "The latest visuals curated by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('art.add_visual'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'art:visual_create',
            )
        return context

class TopVisualListView(ListView):

    model = Visual
    paginate_by = ArtAppProfile.objects.get_or_create(pk=1)[0].visual_list_pagination
    context_object_name = 'visuals'

    def get_queryset(self, *args, **kwargs):
        return Visual.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Visuals"
        # SEO stuff
        context['meta_title'] = "Top Visuals | {}".format(
            profile.title,
        )
        context['meta_desc'] = "Amazing visuals curated by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('art.add_visual'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'art:visual_create',
            )
        return context

class VisualDetailView(DetailView):

    model = Visual
    context_object_name = 'visual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # Galleries that have the visual in their list
        context['galleries'] = Gallery.objects.filter(
            visuals__pk=self.object.pk,
            is_public=True,
        )
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            # Post Actions
            if self.object.owner.pk == member.pk:
                if not self.object.is_public:
                    context['show_publish_button'] = True
                    context['publish_button'] = {
                        'url': reverse(
                            'art:publish_visual',
                            kwargs={
                                'pk': self.object.pk,
                            },
                        )
                    }
                context['show_edit_button'] = True
                context['edit_button'] = {
                     'url': reverse(
                        'art:visual_update',
                        kwargs={
                            'slug': self.object.slug,
                        },
                    )
                }
                context['show_delete_button'] = True
                context['delete_button'] = {
                     'url': reverse(
                        'art:visual_delete',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    )
                }
            # Marshmallow button
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
                context['marshmallow_button'] = {
                    'url': reverse(
                        'art:visual_marshmallow',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    ),
                }
            # Response button
            if self.request.user.has_perms('posts:add_response'):
                context['can_respond'] = True
                context['response_button'] = {
                    'url': reverse(
                        'posts:response_post_create',
                        kwargs={
                            'model': "visual",
                            'pk': self.object.pk,
                            'members_only': False
                        },
                    ),
                }
            # Get the posts that are a response to this post
            context['responses'] = ResponsePost.objects.filter(
                visual=self.object,
                is_public=True,
            ).order_by('weight', '-publication_date')[:5]
        else:
            context['responses'] = ResponsePost.objects.filter(
                post=self.object,
                is_public=True,
                members_only=False,
            ).order_by('weight', '-publication_date')[:5]
        return context

class MemberVisualView(ListView):

    model = Visual
    paginate_by = ArtAppProfile.objects.get_or_create(pk=1)[0].visual_list_pagination
    context_object_name = 'visuals'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return Visual.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else:
            return Visual.objects.filter(
                owner=member,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Visuals"
        context['meta_title'] = "Visuals by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Visuals curated by {} for {}.".format(
            member,
            profile.title,  
        )
        # Create button
        if self.request.user.has_perm('art.add_visual'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'art:visual_create',
            )
        context['member'] = member
        return context

class VisualUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'art.change_visual'
    model = Visual
    form_class = VisualForm

    def get_form_kwargs(self):
        kwargs = super(VisualUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ArtAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this visual.".format(self.object.title)
        return context

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'art:visual_detail',
                kwargs={'slug': self.object.slug},
            )

class VisualDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'art.delete_visual'
    model = Visual

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_visual_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Visual, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Visual)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Visual.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('art:top_visuals'))

def publish_visual_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Visual, pk=pk)
    if request.method == 'GET':
        template = loader.get_template('publish.html')
        context = {'object': instance}
        return render(request, 'publish.html', context)
    elif request.method == 'POST':
        successful = instance.publish(instance, member)
        if successful:
            messages.add_message(
                request,
                messages.INFO,
                '{} has been published'.format(
                    instance,
                )
            )
            return HttpResponseRedirect(
                reverse(
                    'art:visual_detail',
                    kwargs={
                        'slug': instance.slug,
                    }
                )
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                '{} could not be published'.format(
                    instance,
                )
            )
            return HttpResponseRedirect(
                reverse(
                'art:visual_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

