import datetime
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.utils import timezone, text
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from django.views.generic.detail import DetailView
from documentation.models import Article, Story, SupportDocument
from art.models import Gallery, Visual
from music.models import Album, Track
from objects.models import Image, Sound, Video, Code, Link
from posts.models import Post
from .forms import MemberForm, ProfileForm, UserRegistrationForm
from .models import Member, Profile, InviteLink
# Create your views here.

class StudioView(LoginRequiredMixin, TemplateView):

    template_name = 'members/studio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)

        context['member'] = member
        # Visuals
        context['visuals'] = Visual.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Galleries
        context['galleries'] = Gallery.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Tracks
        context['tracks'] = Track.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Albums
        context['albums'] = Album.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Posts
        context['posts'] = Post.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Stories
        context['stories'] = Story.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Articles
        context['articles'] = Article.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        #Documents
        context['support_documents'] = SupportDocument.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Images
        context['images'] = Image.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Sounds
        context['sounds'] = Sound.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:10]
        # Videos
        context['videos'] = Video.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:10]
        # Code
        context['codes'] = Code.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:10]
        # Links
        context['links'] = Link.objects.filter(
            owner=member
        ).order_by( '-creation_date')[:10]
        return context

class MemberListView(ListView):

    model = Member
    context_object_name = 'members'

    class Meta:
        ordering = ['pk']    

class MemberProfileView(DetailView):

    model = Profile
    context_object_name = 'profile'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.object.member
        context['member'] = member
        # Visuals
        context['visuals'] = Visual.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:9]
        # Galleries
        context['galleries'] = Gallery.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Tracks
        context['tracks'] = Track.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Albums
        context['albums'] = Album.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Posts
        context['posts'] = Post.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Stories
        context['stories'] = Story.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Articles
        context['articles'] = Article.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Documents
        context['support_documents'] = SupportDocument.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Images
        context['images'] = Image.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:9]
        # Videos
        context['videos'] = Video.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Sounds
        context['sounds'] = Sound.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Code
        context['codes'] = Code.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
        # Links
        context['links'] = Link.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:3]
    
        return context

class MemberProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = ProfileForm

    def get_form_kwargs(self):
        kwargs = super(MemberProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('members:member_profile', 
                kwargs={'slug': self.object.slug}
            )

class MemberUpdateView(LoginRequiredMixin, UpdateView):

    model = Member
    form_class = MemberForm 

    def form_valid(self, form):
        if self.request.user.pk == self.object.pk:
            return super().form_valid(form)
        else:
            return reverse_lazy('members:member_profile',
                kwargs={'slug': self.object.username}
            )
            
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('members:member_profile',
                kwargs={'slug': self.object.username}
            )

def member_registration(request, *args, **kwargs):
    if request.method == 'POST':
        global invite 
        invite = InviteLink.objects.get(
            pk=request.POST.get('invite'),
        )
        if invite.expiration_date > timezone.now():
            f = UserCreationForm(request.POST)
            if f.is_valid():
                f.save()
                invite.delete()
                messages.success(
                    request,
                    "Welcome! Please log in using your provided credentials."
                )
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.info(
                request,
                "The invite link is expired and can no longer be used."
            )
            return HttpResponseRedirect(reverse('login'))
    return HttpResponseRedirect(
        reverse_lazy(
            'members:invite_link_detail',
            kwargs={
                'slug': invite.slug,
            },
        )
    )

class InviteLinkCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = 'members.add_invitelink'
    model = InviteLink
    fields = ['label', 'note']

    def form_valid(self, form):
        form.instance.slug = self.model.make_slug(form.instance)
        form.instance.expiration_date += datetime.timedelta(days=7)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('members:invite_link_detail', 
            kwargs={'slug': self.object.slug}
        )

class InviteLinkDetailView(FormMixin, DetailView):

    model = InviteLink
    template_name = 'member_registration.html'
    form_class = UserRegistrationForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            invite = InviteLink.objects.get(
                pk=self.object.pk,
            )
            if invite.expiration_date > timezone.now():
                form.save()
                messages.success(
                    request,
                    "Welcome! You are now a member of the site. Please authenticate using your provided credentials.",
                )
                invite.delete()
                return self.form_valid(form)
            else:
                messages.error(
                    request,
                    "This invite link has expired! Please request a new one from the site administrator.",
                )
                invite.delete()
                return reverse('home:index')
        else:
            return self.form_invalid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('login')
