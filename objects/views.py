from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberOwnershipView
from .forms import ImageCreateForm, ImageUpdateForm
from .models import Tag, Image, Sound, Code, Link
# Create your views here.

# Image Views
class ImageCreateView(LoginRequiredMixin, CreateView):

    model = Image
    form_class = ImageCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.member = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:image_detail', kwargs={'pk': self.object.pk})

class ImageListView(ListView):

    model = Image
    paginate_by = 30
    queryset = Image.objects.filter(is_public=True)
    context_object_name = 'public_images'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberImageView(LoginRequiredMixin, ListView):

    model = Image
    paginate_by = 30
    context_object_name = 'member_images'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(pk=self.kwargs['user'].pk)
        return Image.objects.filter(member=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.kwargs['user'].pk)
        context['user_only'] = True
        context['member'] = member
        return context

class ImageDetailView(DetailView):

    model = Image
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ImageUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Image
    form_class = ImageUpdateForm    
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ImageDeleteView(LoginRequiredMixin, MemberOwnershipView, DeleteView):

    model = Image
    success_url = reverse_lazy('objects:member_image_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
