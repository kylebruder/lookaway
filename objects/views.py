from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils import timezone, text
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from documentation.models import Article, SupportDocument
from lookaway.settings import BASE_DIR
from art.models import Gallery, Visual
from members.models import Member
from members.mixins import MemberOwnershipView, MemberDeleteView
from music.models import Album, Track
from posts.models import Post
from .forms import (ImageCreateForm, ImageUpdateForm, SoundCreateForm,
    SoundUpdateForm, VideoCreateForm, VideoUpdateForm, CodeForm, LinkCreateForm, 
    LinkForm, TagForm)
from .models import Tag, Image, Sound, Video, Code, Link
# Create your views here.

# Image Views
class ImageCreateView(LoginRequiredMixin, CreateView):

    model = Image
    form_class = ImageCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        
        member = Member.objects.get(pk=self.request.user.pk)
        # CHeck disk space before uploading
        has_free_space, free, used = member.check_free_media_capacity(
            BASE_DIR + '/media/member_{}/'.format(member.pk),
        )
        upload_size = self.request.FILES['image_file'].size
        print('{}, {}, {}'.format(has_free_space, free, used))
        if has_free_space:
            if free > upload_size:
                messages.add_message(
                    self.request,
                    messages.INFO,
                    '''Upload Successful. Your media directory has {} MB of \
                    free capicity.'''.format(
                        round(free*10**-6),
                    )
                )
                form.instance.creation_date = timezone.now()
                form.instance.owner = member
                # Set default image URLs in case the post_save signal
                # fails for any reason. Missing URLs will break the template
                form.image_file = "#"
                form.thumbnail_file= "#"       
                return super().form_valid(form) 
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    'Upload FAIL: Your media directory only has {} bytes of free capacity. Image file of \
{} bytes is too large.'.format(
                        free,
                        upload_size,
                    ),
                )
                return redirect(reverse('objects:image_create')) 
        else:
            messages.add_message(
                self.request,
                messages.WARNING,
                'Upload FAIL. Your media directory is over capacity.',
            )
            return redirect(reverse('members:studio'))
            
    
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
    paginate_by = 36
    queryset = Image.objects.filter(is_public=True)
    context_object_name = 'images'
    ordering = ['-weight', '-creation_date']

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

class ImageDetailView(LoginRequiredMixin, DetailView):

    model = Image
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
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

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:image_detail', kwargs={'pk': self.object.pk})

class ImageDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_image_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Image, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Image)
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
    return HttpResponseRedirect(reverse('objects:public_images'))

def publish_image_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Image, pk=pk)
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
                    'objects:image_detail',
                    kwargs={
                        'pk': instance.pk,
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
                'objects:image_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# Sound Views
class SoundCreateView(LoginRequiredMixin, CreateView):

    model = Sound
    form_class = SoundCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        has_free_space, free, used = member.check_free_media_capacity(
            BASE_DIR + '/media/member_{}/'.format(member.pk),
        )
        upload_size = self.request.FILES['sound_file'].size
        print('{}, {}, {}'.format(has_free_space, free, used))
        if has_free_space:
            if free > upload_size:
                messages.add_message(
                    self.request,
                    messages.INFO,
                    'Submission accepted. Your media directory has {} MB of free capicity.'.format(
                        round(free*10**-6),
                    )
                )
                form.instance.creation_date = timezone.now()
                form.instance.owner = member
                return super().form_valid(form)
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    'Submission Rejected. Your media directory only has {} bytes of free capacity. Sound file of \
{} bytes is too large.'.format(
                        free,
                        upload_size,
                    ),
                )
                return redirect(reverse('objects:image_create'))
        else:
            messages.add_message(
                self.request,
                messages.WARNING,
                'Submission Rejected. Your media directory is over capacity.',
            )
            return redirect(reverse('members:studio'))

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
    ordering = ['-weight', '-creation_date']

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
        member = Member.objects.get(pk=self.request.user.pk)
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
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

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:sound_detail', kwargs={'pk': self.object.pk})

class SoundDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Sound

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_sound_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Sound, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Sound)
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
    return HttpResponseRedirect(reverse('objects:public_sounds'))

def publish_sound_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Sound, pk=pk)
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
                    'objects:sound_detail',
                    kwargs={
                        'pk': instance.pk,
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
                'objects:sound_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# Video Views
class VideoCreateView(LoginRequiredMixin, CreateView):

    model = Video
    form_class = VideoCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        has_free_space, free, used = member.check_free_media_capacity(
            BASE_DIR + '/media/member_{}/'.format(member.pk),
        )
        upload_size = self.request.FILES['video_file'].size
        print('{}, {}, {}'.format(has_free_space, free, used))
        if has_free_space:
            if free > upload_size:
                messages.add_message(
                    self.request,
                    messages.INFO,
                    'Submission accepted. Your media directory has {} MB of free capicity.'.format(
                        round(free*10**-6),
                    )
                )
                form.instance.creation_date = timezone.now()
                form.instance.owner = member
                return super().form_valid(form)
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    'Submission Rejected. Your media directory only has {} bytes of free capacity. Video file of \
{} bytes is too large.'.format(
                        free,
                        upload_size,
                    ),
                )
                return redirect(reverse('objects:image_create'))
        else:
            messages.add_message(
                self.request,
                messages.WARNING,
                'Submission Rejected. Your media directory is over capacity.',
            )
            return redirect(reverse('members:studio'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:video_detail', kwargs={'pk': self.object.pk})

class VideoListView(LoginRequiredMixin, ListView):

    model = Video
    paginate_by = 30
    queryset = Video.objects.filter(is_public=True)
    context_object_name = 'videos'
    ordering = ['-weight', '-creation_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MemberVideoView(LoginRequiredMixin, ListView):

    model = Video
    paginate_by = 30
    context_object_name = 'videos'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Video.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class VideoDetailView(LoginRequiredMixin, DetailView):

    model = Video
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        return context

class VideoUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Video
    form_class = VideoUpdateForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:video_detail', kwargs={'pk': self.object.pk})

class VideoDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Video

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_video_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Video, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Video)
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
    return HttpResponseRedirect(reverse('objects:public_videos'))

def publish_video_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Video, pk=pk)
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
                    'objects:video_detail',
                    kwargs={
                        'pk': instance.pk,
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
                'objects:video_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

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
    ordering = ['-weight', '-creation_date']

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
        member = Member.objects.get(pk=self.request.user.pk)
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
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

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:code_detail', kwargs={'pk': self.object.pk})

class CodeDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Code

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_code_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Code, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Code)
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
    return HttpResponseRedirect(reverse('objects:public_code'))

def publish_code_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Code, pk=pk)
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
                    'objects:code_detail',
                    kwargs={
                        'pk': instance.pk,
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
                'objects:code_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# Link Views
class LinkCreateView(LoginRequiredMixin, CreateView):

    model = Link
    form_class = LinkCreateForm
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
    ordering = ['-weight', '-creation_date']

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
        member = Member.objects.get(pk=self.request.user.pk)
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
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

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:link_detail', kwargs={'pk': self.object.pk})

class LinkDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Link

    def get_success_url(self):
        return reverse('members:studio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def add_marshmallow_to_link_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Link, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Link)
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
    return HttpResponseRedirect(reverse('objects:public_links'))

def publish_link_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Link, pk=pk)
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
                    'objects:link_detail',
                    kwargs={
                        'pk': instance.pk,
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
                'objects:link_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# Tag Views
class TagCreateView(LoginRequiredMixin, CreateView):

    model = Tag
    form_class = TagForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        if form.instance.value == None and Tag.objects.filter(key=form.instance.key, value=None).count() >= 1:
            messages.add_message(
                self.request,
                messages.WARNING,
                'Tag with Key "{}" and no Value already exists'.format(form.instance.key),
            )
            return HttpResponseRedirect(self.request.path_info)
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

class TagListView(ListView, LoginRequiredMixin):

    model = Tag
    paginate_by = 32
    context_object_name = 'tags'
    ordering = ['-weight', '-pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TagDetailView(DetailView):

    model = Tag
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.object.slug
        context['posts'] = Post.objects.filter(tags__slug__exact=slug)
        context['galleries'] = Gallery.objects.filter(tags__slug__exact=slug)
        context['visuals'] = Visual.objects.filter(tags__slug__exact=slug)
        context['albums'] = Album.objects.filter(tags__slug__exact=slug)
        context['tracks'] = Track.objects.filter(tags__slug__exact=slug)
        context['articles'] = Article.objects.filter(tags__slug__exact=slug)
        context['documents'] = SupportDocument.objects.filter(tags__slug__exact=slug)
        # Tell the template if there are no objects to show non-members
        public_object_count = context['posts'].count() + \
            context['galleries'].count() + \
            context['visuals'].count() + \
            context['albums'].count() + \
            context['tracks'].count() + \
            context['documents'].count() + \
            context['articles'].count()
        if public_object_count <= 0 and not self.request.user.is_authenticated:
            context['no_public_objects'] = True
        # Member only stuff under here
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            context['images'] = Image.objects.filter(tags__slug__exact=slug).filter(is_public=True)
            context['videos'] = Video.objects.filter(tags__slug__exact=slug).filter(is_public=True)
            context['sounds'] = Sound.objects.filter(tags__slug__exact=slug).filter(is_public=True)
            context['codes'] = Code.objects.filter(tags__slug__exact=slug).filter(is_public=True)
            context['links'] = Link.objects.filter(tags__slug__exact=slug).filter(is_public=True)
            if context['images'].count() + context['videos'].count() + context['sounds'].count() + context['codes'].count() + context['links'].count() <= 0:
                context['no_member_objects'] = True
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

        context = super().get_context_data(**kwargs)
        return context

class TagDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    model = Tag
    permission_required = 'objects:delete_tag'

    def get_success_url(self):
        return reverse('members:studio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def add_marshmallow_to_tag_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Tag, pk=pk)
    successful, instance, weight = member.allocate_marshmallow(instance, model=Tag)
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
    return HttpResponseRedirect(reverse('objects:tags'))

# By Tag Views
class VisualByTag(ListView):

    model = Visual
    context_object_name = 'visuals'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        return Visual.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class GalleryByTag(ListView):

    model = Gallery
    context_object_name = 'galleries'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        return Gallery.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class AlbumByTag(ListView):

    model = Album
    context_object_name = 'albums'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        return Album.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class TrackByTag(ListView):

    model = Track
    context_object_name = 'tracks'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        return Track.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class PostByTag(ListView):

    model = Post
    context_object_name = 'posts'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class ArticleByTag(ListView):

    model = Article
    context_object_name = 'articles'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class SupportDocumentByTag(ListView):
    
    model = SupportDocument
    context_object_name = 'documents'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        return SupportDocument.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class ImageByTag(LoginRequiredMixin, ListView):
    
    model = Image
    context_object_name = 'images'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

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
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        print(Sound.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Sound.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class VideoByTag(LoginRequiredMixin, ListView):
    
    model = Video
    context_object_name = 'videos'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        print(Video.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Video.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class CodeByTag(LoginRequiredMixin, ListView):
    
    model = Code
    context_object_name = 'codes'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

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
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        print(Link.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Link.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

