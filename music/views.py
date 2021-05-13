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
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from objects.utils import Text
from .forms import MusicAppProfileForm, MusicPageSectionForm, AlbumForm, TrackForm
from .models import MusicAppProfile, MusicPageSection, Album, Track

# Create your views here.

# Music app profile views
class MusicAppProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'music.change_musicappprofile'
    model = MusicAppProfile
    form_class = MusicAppProfileForm

    def get_form_kwargs(self):
        kwargs = super(MusicAppProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile settings".format(profile.title)
        context['sections'] = MusicPageSection.objects.all().order_by(
            'order',
        )
        # Add music page section button
        if self.request.user.has_perm('music.add_musicpagesection'):
            context['show_music_page_section_add_button'] = True
            context['music_page_section_add_button'] = { 
                'url': reverse(
                    'music:music_page_section_create',
                ),
            }
        # Edit music page section button
        if self.request.user.has_perm('music.change_musicpagesection'):
            context['show_music_page_section_edit_button'] = True
        # Delete music page section button
        if self.request.user.has_perm('music.delete_musicpagesection'):
            context['show_music_page_section_delete_button'] = True
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('music:music_page')

# Landing page
class MusicPageView(TemplateView, AppPageMixin):

    template_name = 'music/music_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        sections = MusicPageSection.objects.filter(
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
        # Create Track button
        if self.request.user.has_perm('music.add_track'):
            context['show_track_add_button'] = True
            context['track_add_button'] = {
                'url': reverse('music:track_create'),
                'text': "+Track",
            }
        # Create Album button
        if self.request.user.has_perm('music.add_album'):
            context['show_album_add_button'] = True
            context['album_add_button'] = {
                'url': reverse('music:album_create'),
                'text': "+Album",
            }
        # Update AppProfile button
        if self.request.user.has_perm('music.change_musicappprofile'):
            context['show_profile_edit_button'] = True
            context['profile_edit_button'] = {
                'url': reverse('music:music_app_profile_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit App"
            }
        # Add music page section button
        if self.request.user.has_perm('music.add_musicpagesection'):
            context['show_music_page_section_add_button'] = True
            context['music_page_section_add_button'] = { 
                'url': reverse(
                    'music:music_page_section_create',
                ),
            }
        # Edit music page section button
        if self.request.user.has_perm('music.change_musicpagesection'):
            context['show_music_page_section_edit_button'] = True
        # Delete music page section button
        if self.request.user.has_perm('music.delete_musicpagesection'):
            context['show_music_page_section_delete_button'] = True
        return context

class MusicPageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'music.add_musicpagesection'
    model = MusicPageSection
    form_class = MusicPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(MusicPageSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
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
                'music:music_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MusicPageSectionDetailView(LoginRequiredMixin, DetailView):

    model = MusicPageSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        # Add music page section button
        if self.request.user.has_perm('music.add_musicpagesection'):
            context['show_music_page_section_add_button'] = True
            context['music_page_section_add_button'] = {
                'url': reverse(
                    'music:music_page_section_create',
                ),
            }
        # Edit music page section button
        if self.request.user.has_perm('music.change_musicpagesection'):
            context['show_music_page_section_edit_button'] = True
        # Delete music page section button
        if self.request.user.has_perm('music.delete_musicpagesection'):
            context['show_music_page_section_delete_button'] = True
        return context

class MusicPageSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'music.change_musicpagesection'
    model = MusicPageSection
    form_class = MusicPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(MusicPageSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
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
                'music:music_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MusicPageSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = 'music.delete_musicpagesection'
    model = MusicPageSection
    context_object_name = "section"

    def get_success_url(self):
        return reverse(
            'music:music_page',
        )
# Album Views
class AlbumCreateView(LoginRequiredMixin, CreateView):

    model = Album
    form_class = AlbumForm

    def get_form_kwargs(self):
        kwargs = super(AlbumCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = Text.slugify_unique(self.model, form.instance.title)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Album"
        context['meta_desc'] = "Submit an Album you wish to publish. Create some Tracks then choose which Tracks will appear on the Album in the form below."
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'music:album_detail',
                kwargs={'slug': self.object.slug},
            )

class AlbumListView(ListView):

    model = Album
    paginate_by = MusicAppProfile.objects.get_or_create(pk=1)[0].album_list_pagination
    context_object_name = 'albums'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Album.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Album.objects.filter(
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Albums"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "New albums released by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('foo.add_album'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'music:album_create',
            )
        return context

class TopAlbumListView(ListView):

    model = Album
    paginate_by = MusicAppProfile.objects.get_or_create(pk=1)[0].album_list_pagination
    context_object_name = 'albums'

    def get_queryset(self, *args, **kwargs):
        return Album.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Albums"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "Top albums released by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('foo.add_album'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'music:album_create',
            )
        return context

class AlbumDetailView(DetailView):

    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class MemberAlbumView(ListView):

    model = Album
    paginate_by = MusicAppProfile.objects.get_or_create(pk=1)[0].album_list_pagination
    context_object_name = 'albums'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return Album.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else:
            return Album.objects.filter(
                owner=member,
                is_public=True,
            ).order_by(
                '-publication_date',
            )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Albums"
        # SEO stuff
        context['meta_title'] = "Albums released by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Music collections released by {} for {}.".format(
            member,
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('music.add_album'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'music:album_create',
            )
        context['member'] = member
        return context

class AlbumUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Album
    form_class = AlbumForm

    def get_form_kwargs(self):
        kwargs = super(AlbumUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this album.".format(self.object.title)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'music:album_detail',
                kwargs={'slug': self.object.slug},
            )

class AlbumDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Album

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_album_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Album, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Album)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Album.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('music:top_albums'))

def publish_album_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Album, pk=pk)
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
                    'music:album_detail',
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
                'music:album_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# Track Views

class TrackCreateView(LoginRequiredMixin, CreateView):

    model = Track
    form_class = TrackForm

    def get_form_kwargs(self):
        kwargs = super(TrackCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if 'sound' in self.request.GET:
            kwargs['sound'] = self.request.GET.get('sound')
        return kwargs

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = Text.slugify_unique(self.model, form.instance.title)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Track"
        context['meta_desc'] = """Submit a Track you wish to publish. \
            First upload a Sound file then choose it in the form below."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy(
                'music:track_detail',
                kwargs={'slug': self.object.slug},
            )

class TrackListView(ListView):

    model = Track
    paginate_by = MusicAppProfile.objects.get_or_create(pk=1)[0].track_list_pagination
    context_object_name = 'tracks'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Track.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Track.objects.filter(
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Tracks"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "New tracks released by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('music.add_track'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'music:track_create',
            )
        return context

class TopTrackListView(ListView):

    model = Track
    paginate_by = MusicAppProfile.objects.get_or_create(pk=1)[0].track_list_pagination
    context_object_name = 'tracks'

    def get_queryset(self, *args, **kwargs):
        return Track.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Tracks"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "Top tracks released by {} contributors.".format(
            profile.title, 
        )
        # Create button
        if self.request.user.has_perm('music.add_track'):
            context['show_create_button'] = True  
            context['create_button_url'] = reverse(
                'music:track_create',
            )
        return context

class TrackDetailView(DetailView):

    model = Track
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        # Albums that have the Track on their list
        context['albums'] = Album.objects.filter(
            tracks__title=self.object.title,
            is_public=True,
        )
        # Check whether or not to display the Marshmallow button
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class MemberTrackView(ListView):

    model = Track
    paginate_by = MusicAppProfile.objects.get_or_create(pk=1)[0].track_list_pagination
    context_object_name = 'tracks'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return Track.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else:
            return Track.objects.filter(
                owner=member,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Tracks"
        # SEO stuff
        context['meta_title'] = "Tracks released by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Music released by {} for {}.".format(
            member,
            profile.title,  
        )
        # Create button
        if self.request.user.has_perm('music.add_track'):
            context['show_create_button'] = True  
            context['create_button_url'] = reverse(
                'music:track_create',
            )
        context['member'] = member
        return context

class TrackUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Track
    form_class = TrackForm

    def get_form_kwargs(self):
        kwargs = super(TrackUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MusicAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this track.".format(self.object.title)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'music:track_detail',
                kwargs={'slug': self.object.slug},
            )

class TrackDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Track

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_track_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Track, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Track)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Track.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('music:top_tracks'))

def publish_track_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Track, pk=pk)
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
                    'music:track_detail',
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
                'music:track_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

