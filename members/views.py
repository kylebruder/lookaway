from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from documentation.models import SupportDocument
from objects.models import Image, Sound, Video, Code, Link
from .forms import ProfileForm
from .models import Member, Profile
# Create your views here.

class StudioView(LoginRequiredMixin, TemplateView):

    template_name = 'members/studio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)

        context['member'] = member
        # Documentation
        context['documents'] = SupportDocument.objects.filter(
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
        context['images'] = Image.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('is_public', '-creation_date')[:16]
        # Videos
        context['videos'] = Video.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('is_public', '-creation_date')[:5]
        # Sounds
        context['sounds'] = Sound.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('is_public', '-creation_date')[:5]
        # Code
        context['codes'] = Code.objects.filter(
            owner=member,
            is_public=True,
        ).order_by('is_public', '-creation_date')[:5]
        # Links
        context['links'] = Link.objects.filter(
            owner=member,
            is_public=True,
        ).order_by( '-creation_date')[:5]
    
        return context

class MemberProfileUpdateView(UpdateView):

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
