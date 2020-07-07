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
from .forms import (ImageCreateForm, ImageUpdateForm, SoundCreateForm,
    SoundUpdateForm, CodeForm)
from .models import Tag, Image, Sound, Code, Link
# Create your views here.

# Image Views
class ImageCreateView(LoginRequiredMixin, CreateView):

    model = Image
    form_class = ImageCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.owner = Member.objects.get(pk=self.request.user.pk)
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
    context_object_name = 'images'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberImageView(LoginRequiredMixin, ListView):

    model = Image
    paginate_by = 30
    context_object_name = 'images'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Image.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
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

def publish_image_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Image, pk=pk)
    successful = instance.publish(instance, member)
    if successful:
        messages.add_message(
            request,
            messages.INFO,
            '{} has been published'.format(
                instance,
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
            'objects:image_detail',
            kwargs={'pk': instance.pk}
        )
    )

# Sound Views
class SoundCreateView(LoginRequiredMixin, CreateView):

    model = Sound
    form_class = SoundCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.owner = Member.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:sound_detail', kwargs={'pk': self.object.pk})

class SoundListView(ListView):

    model = Sound
    paginate_by = 30
    queryset = Sound.objects.filter(is_public=True)
    context_object_name = 'sounds'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberSoundView(LoginRequiredMixin, ListView):

    model = Sound
    paginate_by = 30
    context_object_name = 'sounds'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Sound.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class SoundDetailView(DetailView):

    model = Sound
    context_object_name = 'sound'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SoundUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Sound
    form_class = SoundUpdateForm
    template_name_suffix = '_update_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SoundDeleteView(LoginRequiredMixin, MemberOwnershipView, DeleteView):

    model = Sound
    success_url = reverse_lazy('objects:member_sounds')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def publish_sound_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Sound, pk=pk)
    successful = instance.publish(instance, member)
    if successful:
        messages.add_message(
            request,
            messages.INFO,
            '{} has been published'.format(
                instance,
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
            'objects:sound_detail',
            kwargs={'pk': instance.pk}
        )
    )

# Code Views
class CodeCreateView(LoginRequiredMixin, CreateView):

    model = Code
    form_class = CodeForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.owner = Member.objects.get(pk=self.request.user.pk)
        form.instance.md5 = Code.get_md5(form.instance.code)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:code_detail', kwargs={'pk': self.object.pk})

class CodeListView(ListView):

    model = Code
    paginate_by = 12
    queryset = Code.objects.filter(is_public=True)
    context_object_name = 'codes'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberCodeView(LoginRequiredMixin, ListView):

    model = Code
    paginate_by = 12
    context_object_name = 'codes'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Code.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class CodeDetailView(DetailView):

    model = Code
    context_object_name = 'code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CodeUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Code
    form_class = CodeForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.md5 = Code.get_md5(form.instance.code)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CodeDeleteView(LoginRequiredMixin, MemberOwnershipView, DeleteView):

    model = Code
    success_url = reverse_lazy('objects:member_code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def publish_code_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Code, pk=pk)
    successful = instance.publish(instance, member)
    if successful:
        messages.add_message(
            request,
            messages.INFO,
            '{} has been published'.format(
                instance,
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
            'objects:code_detail',
            kwargs={'pk': instance.pk}
        )
    )



