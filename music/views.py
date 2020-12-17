import math
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils import timezone, text
from django.views.generic.base import TemplateView 
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberUpdateMixin, MemberDeleteMixin
from .forms import AlbumForm, TrackForm
from .models import Album, Track

# Create your views here.

# Album Views

class MusicPageView(TemplateView):

    template_name = 'music/music_page.html'

    def calculate_album_list_length(self, n):
        return round(math.ceil((n/1.5)/2) * 2)

    def get_context_data(self, **kwargs):
        # Number of items to show in each list
        n = 5
        context = super().get_context_data(**kwargs)
        # Albums
        public_albums = Album.objects.filter(is_public=True)
        album_list_length = self.calculate_album_list_length(n)
        if public_albums.count() >= album_list_length:
            # Get the date of the nth newest Album 
            # if there are enough Albums.
            last_new_album_date = public_albums.order_by(
                '-publication_date',
            )[album_list_length - 1].publication_date
            # Get the 5 newest Albums.
            context['new_albums'] = public_albums.order_by(
                '-publication_date',
            )[:self.calculate_album_list_length(n)]
            # Exclude any Album that appears in the new albums list
            # from the top Album list.
            context['top_albums'] = public_albums.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_album_date,
            )[:self.calculate_album_list_length(n)]
        # If there are less than 5 Albums, 
        # include all of them in the new Album list.
        else:
            context['new_albums'] = public_albums.order_by(
                '-publication_date',
            )
        # Tracks
        if self.request.user.is_authenticated:
            public_tracks = Track.objects.filter(is_public=True)
        # Do not send member only Albums to non members
        else:
            public_tracks = Track.objects.filter(
                is_public=True,
                members_only=False,
            )
        if public_tracks.count() >= n:
            # Get the date of the nth newest Track
            # if there are n or more Tracks
            last_new_track_date = public_tracks.order_by(
                '-publication_date',
            )[n-1].publication_date
            context['new_tracks'] = public_tracks.order_by(
                '-publication_date',
            )[:n]
            # Exclude any Album that appears in the new releases list
            # from the top Track list
            context['top_tracks'] = public_tracks.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_track_date,
            )[:n]
        else:
            context['new_tracks'] = public_tracks.order_by(
                '-publication_date',
            )[:n]
        return context

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
        form.instance.slug = text.slugify(form.instance.title)
        return super().form_valid(form)

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
    paginate_by = 6
    context_object_name = 'albums'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Album.objects.filter(
                is_public=True,
            ).order_by(
                '-creation_date',
            )
        else:
            return Album.objects.filter(
                is_public=True,
                members_only=False,
            ).order_by(
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class TopAlbumListView(ListView):

    model = Album
    paginate_by = 6
    context_object_name = 'albums'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Album.objects.filter(
                is_public=True,
            ).order_by(
                '-weight',
                '-creation_date',
            )
        else:
            return Album.objects.filter(
                is_public=True,
                members_only=False,
            ).order_by(
                '-weight',
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context

class AlbumDetailView(DetailView):

    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class MemberAlbumView(ListView):

    model = Album
    paginate_by = 6
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
        context['user_only'] = True
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
        return kwargs

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = text.slugify(form.instance.title)
        return super().form_valid(form)

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
    paginate_by = 5
    context_object_name = 'tracks'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Track.objects.filter(
                is_public=True,
            ).order_by(
                '-creation_date',
            )
        else:
            return Track.objects.filter(
                is_public=True,
                members_only=False,
            ).order_by(
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class TopTrackListView(ListView):

    model = Track
    paginate_by = 5
    context_object_name = 'tracks'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Track.objects.filter(
                is_public=True,
            ).order_by(
                '-weight',
                '-creation_date',
            )
        else:
            return Track.objects.filter(
                is_public=True,
                members_only=False,
            ).order_by(
                '-weight',
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context

class TrackDetailView(DetailView):

    model = Track
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Albums that have the Track on their list
        context['albums'] = Album.objects.filter(tracks__title=self.object.title)
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
    paginate_by = 5
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
        context['user_only'] = True
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

