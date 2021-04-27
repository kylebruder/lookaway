import datetime
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone, text
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, FormMixin, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from lookaway.mixins import AppPageMixin
from home.models import HomeAppProfile
from documentation.models import Article, Story, SupportDocument
from art.models import Gallery, Visual
from home.models import HomeAppProfile
from music.models import Album, Track
from objects.models import Image, Sound, Video, Code, Link
from posts.models import Post, ResponsePost
from .forms import MemberForm, MembersAppProfileForm, MembersPageSectionForm, ProfileForm, ProfileSettingsForm, UserRegistrationForm, MemberProfileSectionForm, InviteLinkCreateForm
from .mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from .models import Member, MembersAppProfile, MembersPageSection, Profile, InviteLink, MemberProfileSection
# Create your views here.

class StudioView(LoginRequiredMixin, TemplateView):

    template_name = 'members/studio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(pk=self.request.user.pk)
        # App profile
        profile, created = Profile.objects.get_or_create(member=member)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = "{}'s Digital Studio".format(profile.member)
        context['meta_desc'] = "Manage your content"

        context['member'] = member
        # Visuals
        context['visuals'] = Visual.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.visual_list_pagination]
        # Galleries
        context['galleries'] = Gallery.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.gallery_list_pagination]
        # Tracks
        context['tracks'] = Track.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.track_list_pagination]
        # Albums
        context['albums'] = Album.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.album_list_pagination]
        # Posts
        context['posts'] = Post.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.post_list_pagination]
        # Responses
        context['responses'] = ResponsePost.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.response_list_pagination]
        # Stories
        # Stories
        context['stories'] = Story.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.story_list_pagination]
        # Articles
        context['articles'] = Article.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.article_list_pagination]
        #Documents
        context['support_documents'] = SupportDocument.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:profile.document_list_pagination]
        # Images
        context['images'] = Image.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:10]
        # Sounds
        context['sounds'] = Sound.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:10]
        # Videos
        context['videos'] = Video.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:10]
        # Code
        context['codes'] = Code.objects.filter(
            owner=member
        ).order_by('is_public', '-last_modified')[:10]
        # Links
        context['links'] = Link.objects.filter(
            owner=member
        ).order_by( '-last_modified')[:10]
        # Check media storage
        has_free, free, used = member.check_free_media_capacity(
            directory='media/member_' + str(member.pk),
        )
        capacity = member.profile.media_capacity
        context['media_capacity'] = round(capacity / 10**6) # In MB
        context['media_used'] = round(used / 10**6) # In MB
        if has_free:
            context['media_percent_used'] = round(used / capacity * 100) # As a %
        else:
            context['media_percent_used'] = 100
        return context

class MembersAppProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'members.change_membersappprofile'
    model = MembersAppProfile
    form_class = MembersAppProfileForm

    def get_form_kwargs(self):
        kwargs = super(MembersAppProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile settings".format(profile.title)
        context['sections'] = MembersPageSection.objects.all().order_by(
            'order',
        )
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('members:members_page')

class MembersPageView(TemplateView, AppPageMixin):

    template_name = 'members/members_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description

        # Sections
        sections = MembersPageSection.objects.filter(
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
        members = Member.objects.filter(
            groups__name="Members",
        ).exclude(
            groups__name="Contributors",
        ).order_by(
            '-date_joined',
        )[:profile.n_members]
        context['members'] = members
        contributors = Member.objects.filter(
            groups__name="Contributors",
        ).order_by('-date_joined')
        context['contributors'] = contributors.all()[:profile.n_contributors]
        # Create Members button
        if self.request.user.has_perm('members.add_members'):
            context['show_member_invite_button'] = True
            context['create_member_invite_url'] = reverse(
                'invite',
            )
        # Update AppProfile button
        if self.request.user.has_perm('members.change_membersappprofile'):
            context['show_edit_profile_button'] = True
            context['edit_profile_url'] = reverse(
                'members:members_app_profile_update',
                kwargs={'pk': 1},
            )
        return context

class MembersPageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'members.add_memberspagesection'
    model = MembersPageSection
    form_class = MembersPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(MembersPageSectionCreateView, self).get_form_kwargs()
        kwargs['order'] = self.request.GET.get('order')
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
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
                'members:members_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MembersPageSectionDetailView(LoginRequiredMixin, DetailView):

    model = MembersPageSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        return context

class MembersPageSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'members.change_memberspagesection'
    model = MembersPageSection
    form_class = MembersPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(MembersPageSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
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
                'members:members_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MembersPageSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = 'members.delete_memberspagesection'
    model = MembersPageSection
    context_object_name = "section"

    def get_success_url(self):
        return reverse(
            'members:members_page',
        )

class MemberListView(ListView):

    model = Member
    context_object_name = 'members'
    queryset = Member.objects.filter(groups__name='Members')

    class Meta:
        ordering = ['-date_joined']    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "{} Members".format(home.title)
        # SEO stuff
        context['meta_title'] = "Members | {}".format(
            home.title,
        )
        context['meta_desc'] = "Members of the {} online community.".format(
            home.title,
        )
        # Create button
        if self.request.user.has_perm('members.add_invitelink'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'invite',
            )
        return context

class ContributorListView(ListView):

    model = Member
    context_object_name = 'members'
    queryset = Member.objects.filter(groups__name='Contributors')

    class Meta:
        ordering = ['-date_joined']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "{} Contributors".format(home.title)
        # SEO stuff
        context['meta_title'] = "Contributors | {}".format(
            home.title,
        )
        context['meta_desc'] = """A community of artists, musicians, writers, \
            philosophers, and researchers contributing content on {}""".format(
            home.title,
        )
        # Create button
        if self.request.user.has_perm('members.add_invitelink'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'invite',
            )
        return context

class ArtistListView(ListView):

    model = Member
    context_object_name = 'members'
    queryset = Member.objects.filter(groups__name='Artists')

    class Meta:
        ordering = ['-date_joined']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "{} Artists".format(home.title)
        # SEO stuff
        context['meta_title'] = "Artists | {}".format(
            home.title,
        )
        context['meta_desc'] = """A community of artists contributing content \
            on {}""".format(
            home.title,
        )
        # Create button
        if self.request.user.has_perm('members.add_invitelink'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'invite',
            )
        return context

class MusicianListView(ListView):

    model = Member
    context_object_name = 'members'
    queryset = Member.objects.filter(groups__name='Musicians')

    class Meta:
        ordering = ['-date_joined']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "{} Musicians".format(home.title)
        # SEO stuff
        context['meta_title'] = "Musicians | {}".format(
            home.title,
        )
        context['meta_desc'] = """A community of musicians contributing content \
            on {}""".format(
            home.title,
        )
        # Create button
        if self.request.user.has_perm('members.add_invitelink'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'invite',
            )
        return context

class WriterListView(ListView):

    model = Member
    context_object_name = 'members'
    queryset = Member.objects.filter(groups__name='Writers')

    class Meta:
        ordering = ['-date_joined']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "{} Writers".format(home.title)
        # SEO stuff
        context['meta_title'] = "Writers | {}".format(
            home.title,
        )
        context['meta_desc'] = """A community of writers contributing content \
            on {}""".format(
            home.title,
        )
        # Create button
        if self.request.user.has_perm('members.add_invitelink'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'invite',
            )
        return context

class StaffListView(ListView):

    model = Member
    context_object_name = 'members'
    queryset = Member.objects.filter(is_staff=True)

    class Meta:
        ordering = ['-date_joined']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "{} Staff Contributors".format(home.title)
        # SEO stuff
        context['meta_title'] = "Staff Contributors | {}".format(
            home.title,
        )
        context['meta_desc'] = """Staff Contributors \
            on {}""".format(
            home.title,
        )
        # Create button
        if self.request.user.has_perm('members.add_invitelink'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'invite',
            )
        return context

class MemberProfileView(DetailView, AppPageMixin):

    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        context['member'] = profile.member
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        sections = MemberProfileSection.objects.filter(
            owner=self.object.member,
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
        # Posts
        context['new_posts'], context['top_posts'] = self.get_sets(
            Post,
            profile.n_posts,
            show_new=profile.show_new_posts,
            show_top=profile.show_top_posts,
            member=self.object.member,
        )
        # Responses
        context['new_responses'], context['top_responses'] = self.get_sets(
            ResponsePost,
            profile.n_responses,
            show_new=profile.show_new_responses,
            show_top=profile.show_top_responses,
            member=self.object.member,
        )
        # Articles
        context['new_articles'], context['top_articles'] = self.get_sets(
            Article,
            profile.n_articles,
            show_new=profile.show_new_articles,
            show_top=profile.show_top_articles,
            member=self.object.member,
        )
        # Stories
        context['new_stories'], context['top_stories'] = self.get_sets(
            Story,
            profile.n_stories,
            show_new=profile.show_new_stories,
            show_top=profile.show_top_stories,
            member=self.object.member,
        )
        # Documents
        context['new_documents'], context['top_documents'] = self.get_sets(
            SupportDocument,
            profile.n_documents,
            show_new=profile.show_new_documents,
            show_top=profile.show_top_documents,
            member=self.object.member,
        )
        # Visuals
        context['new_visuals'], context['top_visuals'] = self.get_sets(
            Visual,
            profile.n_visuals,
            show_new=profile.show_new_visuals,
            show_top=profile.show_top_visuals,
            member=self.object.member,
        )
        # Galleries
        context['new_galleries'], context['top_galleries'] = self.get_sets(
            Gallery,
            profile.n_galleries,
            show_new=profile.show_new_galleries,
            show_top=profile.show_top_galleries,
            member=self.object.member,
        )
        # Tracks
        context['new_tracks'], context['top_tracks'] = self.get_sets(
            Track,
            profile.n_tracks,
            show_new=profile.show_new_tracks,
            show_top=profile.show_top_tracks,
            member=self.object.member,
        )
        # Albums
        context['new_albums'], context['top_albums'] = self.get_sets(
            Album,
            profile.n_albums,
            show_new=profile.show_new_albums,
            show_top=profile.show_top_albums,
            member=self.object.member,
        )

        # Update profile buttons
        if self.request.user == self.object.member:
            context['show_profile_edit_button'] = True
            context['profile_edit_url'] = reverse(
                'members:member_profile_update',
                kwargs={'slug': self.object.member.username},
            )
        if self.request.user.has_perm('members.add_invite'):
            context['show_invite_add_button'] = True

        # Turning these off for now
        ## Images
        #context['images'] = Image.objects.filter(
        #    owner=member,
        #    is_public=True,
        #).order_by('-publication_date')[:9]
        # Videos
        #context['videos'] = Video.objects.filter(
        #    owner=member,
        #    is_public=True,
        #).order_by('-publication_date')[:3]
        # Sounds
        #context['sounds'] = Sound.objects.filter(
        #    owner=member,
        #    is_public=True,
        #).order_by('-publication_date')[:3]
        # Code
        #context['codes'] = Code.objects.filter(
        #    owner=member,
        #    is_public=True,
        #).order_by('-publication_date')[:3]
        # Links
        #context['links'] = Link.objects.filter(
        #    owner=member,
        #    is_public=True,
        #).order_by('-publication_date')[:3]

        return context


class MemberProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = ProfileForm

    def get_form_kwargs(self):
        kwargs = super(MemberProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile = self.object
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile
        context['meta_desc'] = "Update your profile"
        context['sections'] = MemberProfileSection.objects.filter(
            owner=self.request.user
        ).order_by(
            'order',
        )
        return context

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
                kwargs={'slug': self.object.slug}
            )

class MemberProfileSettingsUpdateView(LoginRequiredMixin, UpdateView):

    model = Profile
    form_class = ProfileSettingsForm
    template_name = 'members/memberprofilesettings_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile = self.object
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile
        context['meta_desc'] = "Update your profile display settings"
        return context

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
                kwargs={'slug': self.object.slug}
            )

class MemberProfileSectionCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = MemberProfileSection
    form_class = MemberProfileSectionForm

    def get_form_kwargs(self):
        kwargs = super(MemberProfileSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['order'] = self.request.GET.get('order')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile = get_object_or_404(Profile, member=self.request.user)
        context['profile'] = profile
        context['meta_title'] = "New Profile Page Section"
        context['meta_desc'] = "Add a section to your profile page"
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
                'members:member_profile_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MemberProfileSectionDetailView(LoginRequiredMixin, DetailView):

    model = MemberProfileSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile = get_object_or_404(Profile, member=self.request.user)
        context['profile'] = profile
        context['meta_title'] = profile.title
        return context

class MemberProfileSectionUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = MemberProfileSection
    form_class = MemberProfileSectionForm

    def get_form_kwargs(self):
        kwargs = super(MemberProfileSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile = get_object_or_404(Profile, member=self.request.user)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this profile page section.".format(self.object.title)
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
                'members:member_profile_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MemberProfileSectionDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = MemberProfileSection
    context_object_name = "section"

    def get_success_url(self):
        return reverse(
            'members:member_profile',
            kwargs={'slug': self.object.owner.username}
        )

class MemberUpdateView(LoginRequiredMixin, UpdateView):

    model = Member
    form_class = MemberForm 

    def form_valid(self, form):
        if self.request.user == self.object:
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
    form_class= InviteLinkCreateForm

    def form_valid(self, form):
        form.instance.slug = self.model.make_slug(form.instance)
        form.instance.expiration_date += datetime.timedelta(days=7)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        home, created = HomeAppProfile.objects.get_or_create(pk=1)
        profile, created = MembersAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Invite Link"
        context['meta_desc'] = "Invite someone to join {}".format(home.title)
        return context

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

class PasswordChangeDone(TemplateView):

    template_name = 'members/password_change_done.html'
