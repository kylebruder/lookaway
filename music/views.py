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
from members.mixins import MemberOwnershipView, MemberDeleteView
from .forms import AlbumForm, TrackForm
from .models import Album, Track

# Create your views here.

# Album Views

class MusicPageView(TemplateView):

    template_name = 'music/music_page.html'

    def get_context_data(self, **kwargs):
        # Number of items to show in each list
        n = 5
        context = super().get_context_data(**kwargs)
        # Albums
        if self.request.user.is_authenticated:
            public_albums = Album.objects.filter(is_public=True)
        # Do not send member only Albums to non members
        else:
            public_albums = Album.objects.filter(
                is_public=True,
                members_only=False,
            )
        if public_albums.count() >= n:
            print("There are {} or more published Albums".format(n))
            # Get the date of the 5th newest Album 
            # if there are 5 or more Albums.
            last_new_album_date = public_albums.order_by(
                '-publication_date',
            )[n-1].publication_date
            # Get the 5 newest Albums.
            context['new_albums'] = public_albums.order_by(
                '-publication_date',
            )[:n]
            # Exclude any Album that appears in the new albums list
            # from the top Album list.
            context['top_albums'] = public_albums.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_album_date,
            )[:n]
            print("New Albums: {}".format(context['new_albums']))
            print("Top Albums: {}".format(context['top_albums']))
        # If there are less than 5 Albums, 
        # include all of them in the new Album list.
        else:
            print("There are less than 5 published Albums")
            context['new_albums'] = public_albums.order_by(
                '-publication_date',
            )
            print(context['new_albums'])
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
            print("There are {} or more published Tracks".format(n))
            # Get the date of the nth newest Track
            # if there are n or more Tracks
            last_new_track_date = public_tracks.order_by(
                '-publication_date',
            )[n-1].publication_date
            context['new_tracks'] = public_tracks.order_by(
                '-publication_date',
            )[:n]
            print("New Tracks: ", context['new_tracks'])
            # Exclude any Album that appears in the new releases list
            # from the top Track list
            context['top_tracks'] = public_tracks.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_track_date,
            )[:n]
            print("Top Tracks: ", context['top_tracks'])
        else:
            print("There are less than {} published Tracks".format(n))
            context['new_tracks'] = public_tracks.order_by(
                '-publication_date',
            )[:n]
            print(context['new_tracks'])
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

class TopAlbumListView(ListView):

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class AlbumUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

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

class AlbumDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Album

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_document_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Album, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Album)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave a marshmallow to {} weighing {}'.format(
                    instance,
                    round(weight, 2)
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You failed to give a marshmallow to {}'.format(instance)
            )
    return HttpResponseRedirect(reverse('music:public_albums'))

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
    paginate_by = 6
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

class TopTrackListView(ListView):

    model = Track
    paginate_by = 6
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

class TrackDetailView(DetailView):

    model = Track
    context_object_name = 'track'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class MemberTrackView(ListView):

    model = Track
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

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

class TrackUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

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

class TrackDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Track

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_document_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Track, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Track)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave a marshmallow to {} weighing {}'.format(
                    instance,
                    round(weight, 2)
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You failed to give a marshmallow to {}'.format(instance)
            )
    return HttpResponseRedirect(reverse('music:public_tracks'))

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

