from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from objects.models import Image, Sound, Code, Link
from .models import Member
# Create your views here.

class StudioView(TemplateView):

    template_name = 'members/studio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)

        # Images
        context['member'] = member
        context['images'] = Image.objects.filter(
            owner=member
        ).order_by('is_public', '-creation_date')[:24]
        # Sounds
        context['sounds'] = Sound.objects.filter(
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

class MemberDetailView(DetailView):

    model = Member
    context_object_name = 'member'


