from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils import timezone, text
from django.views.decorators.http import require_POST
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from documentation.models import Article, Story, SupportDocument
from lookaway.mixins import AppPageMixin
from lookaway.settings import BASE_DIR
from home.models import HomeAppProfile
from art.models import Gallery, Visual
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from music.models import Album, Track
from posts.models import Post
from .utils import Text
from .forms import (ObjectsAppProfileForm, ObjectsPageSectionForm, 
    ObjectsAppTranscoderSettingsForm, ImageCreateForm, ImageUpdateForm, 
    SoundCreateForm, SoundUpdateForm, VideoCreateForm, VideoUpdateForm, 
    CodeForm, LinkCreateForm, LinkForm, TagForm)
from .app_profile_mixins import ModelListMixin, ModelByTagMixin, MemberViewMixin, StudioListMixin
from .models import ObjectsAppProfile, ObjectsPageSection, Tag, Image, Sound, Video, Code, Link
# Create your views here.

# Objects App Form
class ObjectsAppProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'objects.change_objectsappprofile'
    model = ObjectsAppProfile
    form_class = ObjectsAppProfileForm

    def get_form_kwargs(self):
        kwargs = super(ObjectsAppProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile".format(profile.title)
        context['sections'] = ObjectsPageSection.objects.all().order_by(
            'order',
        )
        # Add objects page section button
        if self.request.user.has_perm('objects.add_objectspagesection'):
            context['show_objects_page_section_add_button'] = True
            context['objects_page_section_add_button'] = {
                'url': reverse(
                    'objects:objects_page_section_create',
                ),
            }
        # Edit objects page section button
        if self.request.user.has_perm('objects.change_objectspagesection'):
            context['show_objects_page_section_edit_button'] = True
        # Delete objects page section button
        if self.request.user.has_perm('objects.delete_objectspagesection'):
            context['show_objects_page_section_delete_button'] = True
        # Edit objects app settings button
        if self.request.user.has_perm('objects.change_objectsappprofile'):
            context['show_objects_app_profile_settings_edit_button'] = True
            context['objects_app_profile_settings_edit_button'] = {
                'url': reverse(
                    'objects:objects_app_transcoder_settings_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit Settings",
            }
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'objects:objects_page',
            )

# Objects App transcoder form
class ObjectsAppTranscoderSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView, MemberUpdateMixin):

    permission_required = 'objects.change_objectsappprofile'
    model = ObjectsAppProfile
    form_class = ObjectsAppTranscoderSettingsForm
    template_name = 'objects/objects_app_transcoder_settings_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" transcoder settings".format(profile.title)
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:objects_page')

class ObjectsPageView(LoginRequiredMixin, TemplateView, AppPageMixin):

    template_name = 'objects/objects_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        sections = ObjectsPageSection.objects.filter(
            is_enabled = True,
        ).order_by(
            'order',
        )
        if self.request.user.is_authenticated:
            context['sections'] = sections
        else:
            context['sections'] = sections.exclude(
                members_only=True
            )
        # Images
        context['new_images'], context['top_images'] = self.get_sets(
            Image,
            profile.n_images,
            show_new=profile.show_images,
            show_top=profile.show_images,
        )
        # Sounds
        context['new_sounds'], context['top_sounds'] = self.get_sets(
            Sound,
            profile.n_sounds,
            show_new=profile.show_sounds,
            show_top=profile.show_sounds,
        )
        # Videos
        context['new_videos'], context['top_videos'] = self.get_sets(
            Video,
            profile.n_videos,
            show_new=profile.show_videos,
            show_top=profile.show_videos,
        )
        # Code
        context['new_codes'], context['top_codes'] = self.get_sets(
            Code,
            profile.n_codes,
            show_new=profile.show_codes,
            show_top=profile.show_codes,
        )
        # Links
        context['new_links'], context['top_links'] = self.get_sets(
            Link,
            profile.n_links,
            show_new=profile.show_links,
            show_top=profile.show_links,
        )
        # Create Objects button
        if self.request.user.has_perm('objects.add_objects'):
            context['show_member_invite_button'] = True
            context['create_member_invite_url'] = reverse(
                'invite',
            )
        # Update AppProfile button
        if self.request.user.has_perm('objects.change_objectsappprofile'):
            context['show_profile_edit_button'] = True
            context['profile_edit_button'] = {
                'url': reverse(
                    'objects:objects_app_profile_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit App",
            }
        # Add objects page section button
        if self.request.user.has_perm('objects.add_objectspagesection'):
            context['show_objects_page_section_add_button'] = True
            context['objects_page_section_add_button'] = {
                'url': reverse(
                    'objects:objects_page_section_create',
                ),
            }
        # Edit objects page section button
        if self.request.user.has_perm('objects.change_objectspagesection'):
            context['show_objects_page_section_edit_button'] = True
        # Delete objects page section button
        if self.request.user.has_perm('objects.delete_objectspagesection'):
            context['show_objects_page_section_delete_button'] = True
        # Edit objects app settings button
        if self.request.user.has_perm('objects.change_objectsappprofile'):
            context['show_objects_app_profile_settings_edit_button'] = True
            context['objects_app_profile_settings_edit_button'] = {
                'url': reverse(
                    'objects:objects_app_transcoder_settings_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit Settings",
            }
        return context

class ObjectsPageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'objects.add_objectspagesection'
    model = ObjectsPageSection
    form_class = ObjectsPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(ObjectsPageSectionCreateView, self).get_form_kwargs()
        kwargs['order'] = self.request.GET.get('order')
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Page Section"
        context['meta_desc'] = "Add a section to the {} landing page.".format(profile.title)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'objects:objects_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class ObjectsPageSectionDetailView(LoginRequiredMixin, DetailView):

    model = ObjectsPageSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        context['sections'] = True
        # Add objects page section button
        if self.request.user.has_perm('objects.add_objectspagesection'):
            context['show_objects_page_section_add_button'] = True
            context['objects_page_section_add_button'] = {
                'url': reverse(
                    'objects:objects_page_section_create',
                ),
            }
        # Edit objects page section button
        if self.request.user.has_perm('objects.change_objectspagesection'):
            context['show_objects_page_section_edit_button'] = True
        # Delete objects page section button
        if self.request.user.has_perm('objects.delete_objectspagesection'):
            context['show_objects_page_section_delete_button'] = True
        # Edit objects app settings button
        if self.request.user.has_perm('objects.change_objectsappprofile'):
            context['show_objects_app_profile_settings_edit_button'] = True
            context['objects_app_profile_settings_edit_button'] = {
                'url': reverse(
                    'objects:objects_app_transcoder_settings_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit Settings",
            }
        return context

class ObjectsPageSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'objects.change_objectspagesection'
    model = ObjectsPageSection
    form_class = ObjectsPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(ObjectsPageSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this landing page section.".format(self.object.title)
        return context

    def form_valid(self, form):
        # Update last modified date for the Section
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'objects:objects_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class ObjectsPageSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = 'objects.delete_objectspagesection'
    model = ObjectsPageSection
    context_object_name = "section"

    def get_success_url(self):
        return reverse(
            'objects:objects_page',
        )

# Image Views
class ImageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Image
    permission_required = 'objects.add_image'
    form_class = ImageCreateForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        
        member = Member.objects.get(pk=self.request.user.pk)
        # Check disk space before uploading
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
                    '''Image upload successful. Your media directory has {} MB of \
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

    def get_from_kwargs(self):
        kwargs = super(ImageUpdateView, self).get_from_kwargs()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Upload an Image File"
        context['meta_desc'] = """Submit an Image you wish to upload. Images \
            will be optimized for web performance. Keep all originals."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('objects:image_detail', kwargs={'pk': self.object.pk})

class ImageListView(ModelListMixin, LoginRequiredMixin, ListView):

    model = Image
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].images_list_pagination
    except:
        paginate_by = 30
    queryset = Image.objects.filter(is_public=True)
    context_object_name = 'images'
    ordering = ['-weight', '-creation_date']
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_image'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:image_create',
            )
        return context

class MemberImageView(MemberViewMixin, LoginRequiredMixin, ListView):

    model = Image
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].images_list_pagination
    except:
        paginate_by = 30
    context_object_name = 'images'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_image'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:image_create',
            )
        context['member'] = Member.objects.get(username=self.kwargs['member'])
        return context

class ImageStudioListView(StudioListMixin, LoginRequiredMixin, ListView):

    model = Image
    template_name = 'objects/studio_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_image'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:image_create',
            )
        return context
    
class ImageDetailView(LoginRequiredMixin, DetailView):

    model = Image
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        if self.request.user.has_perm('art.add_visual') and self.request.user.pk == self.object.owner.pk:
            context['show_visual_add_button'] = True
            context['visual_add_button'] = {
                'url': reverse('art:visual_create'),
                'parameters': "?image={}".format(self.object.pk),
                'text': "+Visual",
            }
        return context

class ImageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Image
    permission_required = 'objects.change_image'
    form_class = ImageUpdateForm    
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this Image."
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:image_detail', kwargs={'pk': self.object.pk})

class ImageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Image
    permission_required = 'objects.delete_image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_image_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Image, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Image)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Image.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
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
class SoundCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Sound
    permission_required = 'objects.add_sound'
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
                    'Sound upload was successful. Your media directory has {} MB of free capicity.'.format(
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
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Upload a Sound File"
        context['meta_desc'] = """Submit a sound file you wish to upload. Sounds \
            will be optimized for web performance. Keep all originals."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:sound_detail', kwargs={'pk': self.object.pk})

class SoundListView(ModelListMixin, LoginRequiredMixin, ListView):

    model = Sound
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].sounds_list_pagination
    except:
        paginate_by = 100
    queryset = Sound.objects.filter(is_public=True)
    context_object_name = 'sounds'
    ordering = ['-weight', '-creation_date']
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_sound'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:sound_create',
            )
        return context

class MemberSoundView(MemberViewMixin, LoginRequiredMixin, ListView):

    model = Sound
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].sounds_list_pagination
    except:
        paginate_by = 100
    context_object_name = 'sounds'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_sound'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:sound_create',
            )
        context['member'] = Member.objects.get(username=self.kwargs['member'])
        return context

class SoundStudioListView(StudioListMixin, LoginRequiredMixin, ListView):

    model = Sound
    template_name = 'objects/studio_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_sound'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:sound_create',
            )
        return context

class SoundDetailView(LoginRequiredMixin, DetailView):

    model = Sound
    context_object_name = 'sound'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        if self.request.user.has_perm('music.add_track') and self.request.user.pk == self.object.owner.pk:
            context['show_track_add_button'] = True
            context['track_add_button'] = {
                'url': reverse('music:track_create'),
                'parameters': "?sound={}".format(self.object.pk),
                'text': "+Track",
            }
        return context

class SoundUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Sound
    permission_required = 'objects.change_sound'
    form_class = SoundUpdateForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this Sound."
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:sound_detail', kwargs={'pk': self.object.pk})

class SoundDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Sound
    permission_required = 'objects.delete_sound'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_sound_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Sound, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Sound)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Sound.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
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
class VideoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Video
    permission_required = 'objects.add_video'
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
                    'Video upload was successful. Your media directory has {} MB of free capicity.'.format(
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
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Upload a Video File"
        context['meta_desc'] = """Submit a Video you wish to upload. Videos \
            will be optimized for web performance. Keep all originals."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:video_detail', kwargs={'pk': self.object.pk})

class VideoListView(ModelListMixin, LoginRequiredMixin, ListView):

    model = Video
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].videos_list_pagination
    except:
        paginate_by = 100
    queryset = Video.objects.filter(is_public=True)
    context_object_name = 'videos'
    ordering = ['-weight', '-creation_date']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_video'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:video_create',
            )
        return context

class MemberVideoView(MemberViewMixin, LoginRequiredMixin, ListView):

    model = Video
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].videos_list_pagination
    except:
        paginate_by = 100
    context_object_name = 'videos'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_video'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:video_create',
            )
        context['member'] = Member.objects.get(username=self.kwargs['member'])
        return context

class VideoStudioListView(StudioListMixin, LoginRequiredMixin, ListView):

    model = Video
    template_name = 'objects/studio_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_video'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:video_create',
            )
        return context

class VideoDetailView(LoginRequiredMixin, DetailView):

    model = Video
    context_object_name = 'video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        return context

class VideoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Video
    permission_required = 'objects.change_video'
    form_class = VideoUpdateForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this Video."
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:video_detail', kwargs={'pk': self.object.pk})

class VideoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Video
    permission_required = 'objects.delete_video'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_video_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Video, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Video)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Video.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
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
class CodeCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    model = Code
    permission_required = 'objects.add_code'
    form_class = CodeForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.owner = Member.objects.get(pk=self.request.user.pk)
        form.instance.md5 = Code.get_md5(form.instance.code)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Code Sample"
        context['meta_desc'] = """Add a sample of code that can be added to \
            your pages."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:code_detail', kwargs={'pk': self.object.pk})

class CodeListView(ModelListMixin, LoginRequiredMixin, ListView):

    model = Code
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].codes_list_pagination
    except:
        paginate_by = 100
    context_object_name = 'codes'
    ordering = ['-weight', '-creation_date']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_code'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:code_create',
            )
        return context

class MemberCodeView(MemberViewMixin, LoginRequiredMixin, ListView):

    model = Code
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].codes_list_pagination
    except:
        paginate_by = 100
    context_object_name = 'codes'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_code'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:code_create',
            )
        context['member'] = Member.objects.get(username=self.kwargs['member'])
        return context

class CodeStudioListView(StudioListMixin, LoginRequiredMixin, ListView):

    model = Code
    template_name = 'objects/studio_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_code'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:code_create',
            )
        return context

class CodeDetailView(LoginRequiredMixin, DetailView):

    model = Code
    context_object_name = 'code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        return context

class CodeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Code
    permission_required = 'objects.change_code'
    form_class = CodeForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        form.instance.md5 = Code.get_md5(form.instance.code)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        
        context['meta_desc'] = "Make changes to this code sample."
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:code_detail', kwargs={'pk': self.object.pk})

class CodeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Code
    permission_required = 'objects.code_delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_code_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Code, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Code)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Code.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
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
class LinkCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    model = Link
    permission_required = 'objects.add_link'
    form_class = LinkCreateForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.creation_date = timezone.now()
        form.instance.owner = Member.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Link"
        context['meta_desc'] = """Add a link to an external website."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:link_detail', kwargs={'pk': self.object.pk})

class LinkListView(ModelListMixin, LoginRequiredMixin, ListView):

    model = Link
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].links_list_pagination
    except:
        paginate_by = 100
    queryset = Link.objects.filter(is_public=True)
    context_object_name = 'links'
    ordering = ['-weight', '-creation_date']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_link'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:link_create',
            )
        return context

class MemberLinkView(MemberViewMixin, LoginRequiredMixin, ListView):

    model = Link
    try:
        paginate_by = ObjectsAppProfile.objects.get_or_create(pk=1)[0].links_list_pagination
    except:
        paginate_by = 100
    context_object_name = 'links'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_link'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:link_create',
            )
        context['member'] = Member.objects.get(username=self.kwargs['member'])
        return context

class LinkStudioListView(StudioListMixin, LoginRequiredMixin, ListView):

    model = Link
    template_name = 'objects/studio_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('objects.add_link'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'objects:link_create',
            )
        return context

class LinkDetailView(LoginRequiredMixin, DetailView):

    model = Link
    context_object_name = 'link'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if member.check_can_allocate() and not member.check_is_new():
            context['can_add_marshmallow'] = True
        else:
            context['can_add_marshmallow'] = False
        return context

class LinkUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Link
    permission_required = 'objects.change_link'
    form_class = LinkForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update Link"
        context['meta_desc'] = """Change the URL and information about a link."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:link_detail', kwargs={'pk': self.object.pk})

class LinkDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Link
    permission_required = 'objects.delete_link'

    def get_success_url(self):
        return reverse('members:studio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def add_marshmallow_to_link_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Link, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Link)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Link.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
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
class TagCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    model = Tag
    permission_required = 'objects.add_tag'
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
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Tag"
        context['meta_desc'] = """Add a Tag that can be attached to any site object."""
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('objects:tag_detail', kwargs={'slug': self.object.slug})

class TagListView(ListView, LoginRequiredMixin):

    model = Tag
    paginate_by = 150
    context_object_name = 'tags'
    ordering = ['-weight', '-pk']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TagDetailView(DetailView):

    model = Tag
    context_object_name = 'tag'
    list_length = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.object.slug
        # App profile
        profile, created = ObjectsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # Send the desired list length
        context['list_length'] = self.list_length
        ## Send object lists based on whether the requester is authenticated.
        ## If they are, show them their unpublished objects that match the tag.
        # Posts
        if self.request.user.is_authenticated:
            posts = Post.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            posts = Post.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_posts'] = posts.count()
        context['posts'] = posts[:self.list_length]
        # Art
        if self.request.user.is_authenticated:
            galleries = Gallery.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            galleries = Gallery.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_galleries'] = galleries.count()
        context['galleries'] = galleries[:self.list_length]
        if self.request.user.is_authenticated:
            visuals = Visual.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            visuals = Visual.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_visuals'] = visuals.count()
        context['visuals'] = visuals[:self.list_length]
        if self.request.user.is_authenticated:
            albums = Album.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            albums = Album.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_albums'] = albums.count()
        context['albums'] = albums[:self.list_length]
        if self.request.user.is_authenticated:
            tracks = Track.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            tracks = Track.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_tracks'] = tracks.count()
        context['tracks'] = tracks[:self.list_length]
        # Documentation
        if self.request.user.is_authenticated:
            stories = Story.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            stories = Story.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_stories'] = stories.count()
        context['stories'] = stories[:self.list_length]
        if self.request.user.is_authenticated:
            articles = Article.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            articles = Article.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_articles'] = articles.count()
        context['articles'] = articles[:self.list_length]
        if self.request.user.is_authenticated:
            documents = SupportDocument.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
                tags__slug__exact=slug,
            ).order_by(
                'is_public',
                '-weight',
            )
        else:
            documents = SupportDocument.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by(
                '-weight',
            )
        context['total_documents'] = documents.count()
        context['documents'] = documents[:self.list_length]
        # Tell the template if there are no objects to show non-members
        public_object_count = context['posts'].count() + \
            context['stories'].count() + \
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
            context['images'] = Image.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by('-weight')[:self.list_length]
            context['total_images'] = Image.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).count()
            context['videos'] = Video.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by('-weight')[:self.list_length]
            context['total_videos'] = Video.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).count()
            context['sounds'] = Sound.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by('-weight')[:self.list_length]
            context['total_sounds'] = Sound.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).count()
            context['codes'] = Code.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).order_by('-weight')[:self.list_length]
            context['total_codes'] = Code.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).count()
            context['links'] = Link.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
                ).order_by('-weight')[:self.list_length]
            context['total_links'] = Link.objects.filter(
                tags__slug__exact=slug,
                is_public=True,
            ).count()
            if context['images'].count() + \
                context['videos'].count() + \
                context['sounds'].count() + \
                context['codes'].count() + \
                context['links'].count() <= 0:
                context['no_member_objects'] = True
        return context

class TagUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    model = Tag
    permission_required = 'objects.change_tag'
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
    successful, weight, amount = member.allocate_marshmallow(instance, model=Image)
    if successful:
        messages.add_message(
            request, messages.INFO,
            'You gave {} to the {} "{}"'.format(
                amount,
                Tag.__name__,
                instance,
            )
       )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            'You are not allowed to give marshmallows at this time'
        )
    return HttpResponseRedirect(reverse('objects:tags'))

@require_POST
def get_tag_detail(request, *args, **kwargs):
    return HttpResponseRedirect(
        reverse(
            'objects:tag_detail',
            args=[
                Tag.objects.get(pk=request.POST['pk']).slug,
            ],
        )
    )

# By Tag Views
class VisualByTag(ModelByTagMixin, ListView):

    model = Visual
    context_object_name = 'visuals'
    paginate_by = 32

class GalleryByTag(ModelByTagMixin, ListView):

    model = Gallery
    context_object_name = 'galleries'
    paginate_by = 5

class AlbumByTag(ModelByTagMixin, ListView):

    model = Album
    context_object_name = 'albums'
    paginate_by = 5

class TrackByTag(ModelByTagMixin, ListView):

    model = Track
    context_object_name = 'tracks'
    paginate_by = 5

class PostByTag(ModelByTagMixin, ListView):

    model = Post
    context_object_name = 'posts'
    paginate_by = 5

class ArticleByTag(ModelByTagMixin, ListView):

    model = Article
    context_object_name = 'articles'
    paginate_by = 5

class StoryByTag(ModelByTagMixin, ListView):

    model = Story
    context_object_name = 'stories'
    paginate_by = 5

class SupportDocumentByTag(ModelByTagMixin, ListView):
    
    model = SupportDocument
    context_object_name = 'documents'
    paginate_by = 5

class ImageByTag(ModelByTagMixin, LoginRequiredMixin, ListView):
    
    model = Image
    context_object_name = 'images'
    paginate_by = 32
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        #print(Image.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Image.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class SoundByTag(ModelByTagMixin, LoginRequiredMixin, ListView):
    
    model = Sound
    context_object_name = 'sounds'
    paginate_by = 6
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        #print(Sound.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Sound.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class VideoByTag(ModelByTagMixin, LoginRequiredMixin, ListView):
    
    model = Video
    context_object_name = 'videos'
    paginate_by = 6
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        #print(Video.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Video.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class CodeByTag(ModelByTagMixin, LoginRequiredMixin, ListView):
    
    model = Code
    context_object_name = 'codes'
    paginate_by = 6
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        #print(Code.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Code.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

class LinkByTag(ModelByTagMixin, LoginRequiredMixin, ListView):
    
    model = Link
    context_object_name = 'links'
    paginate_by = 6
    ordering = ['-weight', '-creation_date']

    def get_queryset(self, *args, **kwargs):
        #print(Link.objects.filter(tags__slug__exact=self.kwargs['slug']))
        return Link.objects.filter(tags__slug__exact=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context

