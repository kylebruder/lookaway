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
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from django.views.generic.detail import DetailView
from documentation.models import Document, SupportDocument
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
        # Posts
        context['posts'] = Post.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
        # Documentation
        context['documents'] = Document.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:16]
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

class MemberProfileView(DetailView):

    model = Profile
    context_object_name = 'profile'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = self.object.member
        context['member'] = member
        # Posts
        context['posts'] = Post.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:5]
        # Documentation
        context['documents'] = SupportDocument.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:5]
        context['support_documents'] = SupportDocument.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:5]
        # Images
        context['images'] = Image.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:16]
        # Videos
        context['videos'] = Video.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:5]
        # Sounds
        context['sounds'] = Sound.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:5]
        # Code
        context['codes'] = Code.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:5]
        # Links
        context['links'] = Link.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('-publication_date')[:5]
    
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
