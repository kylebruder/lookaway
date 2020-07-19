from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone, text
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberOwnershipView, MemberDeleteView
from .forms import (ImageCreateForm, ImageUpdateForm, SoundCreateForm,
    SoundUpdateForm, CodeForm, LinkForm, TagForm)
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

class ImageListView(LoginRequiredMixin, ListView):

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

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ImageDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

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

class SoundListView(LoginRequiredMixin, ListView):

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

class SoundDetailView(LoginRequiredMixin, DetailView):

    model = Sound
    context_object_name = 'sound'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SoundUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Sound
    form_class = SoundUpdateForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SoundDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Sound

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

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

class CodeListView(LoginRequiredMixin, ListView):

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

class CodeDetailView(LoginRequiredMixin, DetailView):

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
        form.instance.last_modified = timezone.now()
        form.instance.md5 = Code.get_md5(form.instance.code)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CodeDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Code

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

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


# Link Views
class LinkCreateView(LoginRequiredMixin, CreateView):

    model = Link
    form_class = LinkForm
    template_name_suffix = '_form'

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
            return reverse('objects:link_detail', kwargs={'pk': self.object.pk})

class LinkListView(LoginRequiredMixin, ListView):

    model = Link
    paginate_by = 32
    queryset = Link.objects.filter(is_public=True)
    context_object_name = 'links'
    ordering = ['-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberLinkView(LoginRequiredMixin, ListView):

    model = Link
    paginate_by = 12
    context_object_name = 'links'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Link.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class LinkDetailView(LoginRequiredMixin, DetailView):

    model = Link
    context_object_name = 'link'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LinkUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Link
    form_class = LinkForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LinkDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Link

    def get_success_url(self):
        return reverse('members:studio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def publish_link_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Link, pk=pk)
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
            'objects:link_detail',
            kwargs={'pk': instance.pk}
        )
    )


# Tag Views
class TagCreateView(LoginRequiredMixin, CreateView):

    model = Tag
    form_class = TagForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        if form.instance.value:
            form.instance.slug = text.slugify(
                "{}-{}".format(form.instance.key, form.instance.value)
            )
        else:
            form.instance.slug = text.slugify(form.instance.key)
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
            return reverse('objects:tag_detail', kwargs={'slug': self.object.slug})

class TagListView(LoginRequiredMixin, ListView):

    model = Tag
    paginate_by = 32
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TagDetailView(LoginRequiredMixin, DetailView):

    model = Tag
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.object.slug
        print(slug)
        context['images'] = Image.objects.filter(tags__slug__exact=slug)
        context['sounds'] = Sound.objects.filter(tags__slug__exact=slug)
        context['codes'] = Code.objects.filter(tags__slug__exact=slug)
        context['links'] = Link.objects.filter(tags__slug__exact=slug)
        return context

class TagUpdateView(LoginRequiredMixin, UpdateView):

    model = Tag
    form_class = TagForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        if form.instance.value:
            form.instance.slug = text.slugify(
                "{}-{}".format(form.instance.key, form.instance.value)
            )
        else:
            form.instance.slug = text.slugify(form.instance.key)
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('objects:tag_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TagDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Tag

    def get_success_url(self):
        return reverse('members:studio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# By Tag Views
class ImageByTag(LoginRequiredMixin, ListView):
    
    model = Image
    context_object_name = 'images'
    paginate_by = 32

    def get_queryset(self, *args, **kwargs):
        print(Image.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Image.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class SoundByTag(LoginRequiredMixin, ListView):
    
    model = Sound
    context_object_name = 'sounds'
    paginate_by = 32

    def get_queryset(self, *args, **kwargs):
        print(Sound.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Sound.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class CodeByTag(LoginRequiredMixin, ListView):
    
    model = Code
    context_object_name = 'codes'
    paginate_by = 32

    def get_queryset(self, *args, **kwargs):
        print(Code.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Code.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class LinkByTag(LoginRequiredMixin, ListView):
    
    model = Link
    context_object_name = 'links'
    paginate_by = 32

    def get_queryset(self, *args, **kwargs):
        print(Link.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Link.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context
