from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from lookaway.mixins import AppPageMixin
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from art.models import Visual, Gallery
from documentation.models import Article, Story, SupportDocument
from music.models import Track, Album
from objects.utils import Text
from .forms import PostsAppProfileForm, PostsPageSectionForm, PostForm, ResponsePostForm, ReportPostForm
from .models import PostsAppProfile, PostsPageSection, Post, ResponsePost, ReportPost

# Create your views here.

class PostsAppProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'posts.change_postsappprofile'
    model = PostsAppProfile
    form_class = PostsAppProfileForm

    def get_form_kwargs(self):
        kwargs = super(PostsAppProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile settings".format(profile.title)
        context['sections'] = PostsPageSection.objects.all().order_by(
            'order',
        )
        # Add posts page section button
        if self.request.user.has_perm('posts.add_postspagesection'):
            context['show_posts_page_section_add_button'] = True
            context['posts_page_section_add_button'] = { 
                'url': reverse(
                    'posts:posts_page_section_create',
                ),
            }
        # Edit posts page section button
        if self.request.user.has_perm('posts.change_postspagesection'):
            context['show_posts_page_section_edit_button'] = True
        # Delete posts page section button
        if self.request.user.has_perm('posts.delete_postspagesection'):
            context['show_posts_page_section_delete_button'] = True

        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('posts:posts_page')

class PostsPageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'posts.add_postspagesection'
    model = PostsPageSection
    form_class = PostsPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(PostsPageSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['order'] = self.request.GET.get('order')
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
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
                'posts:posts_page_section_detail',
                kwargs={'pk': self.object.pk},
            )
# Posts app landing page
class PostsPageView(TemplateView, AppPageMixin):

    template_name = 'posts/posts_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        sections = PostsPageSection.objects.filter(
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
        # New and top Post instances
        context['new_posts'], context['top_posts'] = self.get_sets(
            Post,
            profile.n_posts,
            show_new=profile.show_new_posts,
            show_top=profile.show_top_posts,
        )
        # New and top Response instances
        context['new_responses'], context['top_responses'] = self.get_sets(
            ResponsePost,
            profile.n_responses,
            show_new=profile.show_new_responses,
            show_top=profile.show_top_responses,
        )
        # Create Post button
        if self.request.user.has_perm('posts.add_post'):
            context['show_post_add_button'] = True
            context['add_post_button'] = {
                'url': reverse('posts:post_create'),
                'text': "+Post",
            }
        # Update AppProfile button
        if self.request.user.has_perm('posts.change_postsappprofile'):
            context['show_profile_edit_button'] = True
            context['profile_edit_button'] = {
                'url': reverse('posts:posts_app_profile_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit App"
            }
        # Add posts page section button
        if self.request.user.has_perm('posts.add_postspagesection'):
            context['show_posts_page_section_add_button'] = True
            context['posts_page_section_add_button'] = { 
                'url': reverse(
                    'posts:posts_page_section_create',
                ),
            }
        # Edit posts page section button
        if self.request.user.has_perm('posts.change_postspagesection'):
            context['show_posts_page_section_edit_button'] = True
        # Delete posts page section button
        if self.request.user.has_perm('posts.delete_postspagesection'):
            context['show_posts_page_section_delete_button'] = True
        return context

class PostsPageSectionDetailView(LoginRequiredMixin, DetailView):

    model = PostsPageSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        # Add posts page section button
        if self.request.user.has_perm('posts.add_postspagesection'):
            context['show_posts_page_section_add_button'] = True
            context['posts_page_section_add_button'] = {
                'url': reverse(
                    'posts:posts_page_section_create',
                ),
            }
        # Edit posts page section button
        if self.request.user.has_perm('posts.change_postspagesection'):
            context['show_posts_page_section_edit_button'] = True
        # Delete posts page section button
        if self.request.user.has_perm('posts.delete_postspagesection'):
            context['show_posts_page_section_delete_button'] = True

        return context

class PostsPageSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'posts.change_postspagesection'
    model = PostsPageSection
    form_class = PostsPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(PostsPageSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
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
                'posts:posts_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class PostsPageSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    
    permission_required = 'posts.delete_postspagesection'
    model = PostsPageSection
    context_object_name = "section"
    
    def get_success_url(self):
        return reverse(
            'posts:posts_page',
        )

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'posts.add_post'
    model = Post
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = """Submit a Post you wish to publish. Posts \
            are open ended and can contain your contributed media."""
        context['meta_desc'] = "Enter the form instructions here"
        return context

    def form_valid(self, form):
        member = self.request.user
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = Text.slugify_unique(self.model, form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'posts:post_detail',
                kwargs={'slug': self.object.slug},
            )

class PostListView(ListView):

    model = Post
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].post_list_pagination
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Post.objects.filter(
                Q(is_public=True) | Q(members_only=False),
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Posts"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "Recent posts by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('posts.add_post'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'posts:post_create',
            )
        return context
    
class TopPostListView(ListView):

    model = Post
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].post_list_pagination
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(is_public=True),
            ).order_by(
                '-weight',
                '-publication_date',
            )
        else:
            return Post.objects.filter(
                Q(is_public=True) | Q(members_only=False)
            ).order_by(
                '-weight',
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Posts"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "The best posts by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('posts.add_post'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'posts:post_create',
            )
        return context

class MemberPostView(ListView):

    model = Post
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        member = self.request.user
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else: 
            return Post.objects.filter(
                owner=member,
                members_only=False,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Posts"
        context['meta_title'] = "Posts by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Posts by {} on {}.".format(
            member,
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('posts.add_post'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'posts:post_create',
            )
        context['member'] = member
        return context

class PostDetailView(DetailView):

    model = Post
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
            # Get the posts that are a response to this post
            context['responses'] = ResponsePost.objects.filter(
                post=self.object,
                is_public=True,
            ).order_by('weight', '-publication_date')[:5]
            if self.request.user.has_perms('posts:add_response'):
                context['can_add_response'] = True
        else:
            context['responses'] = ResponsePost.objects.filter(
                post=self.object,
                is_public=True,
                members_only=False,
            ).order_by('weight', '-publication_date')[:5]
        return context

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'posts.change_post'
    model = Post
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this Post."
        return context

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'posts:post_detail',
                kwargs={'slug': self.object.slug},
            )

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required  = 'posts.delete_post'
    model = Post

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_post_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Post, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Post)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Post.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('posts:public_posts'))

def publish_post_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Post, pk=pk)
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
                    'posts:post_detail',
                    kwargs={
                        'slug': instance.slug,
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
                'posts:post_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

class ResponsePostCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'posts:add_responsepost'
    model = ResponsePost
    form_class = ResponsePostForm

    def get_target(self):
        model = self.kwargs['model']
        pk = self.kwargs['pk']
        if model == 'post':
            target = Post.objects.get(pk=pk)
        elif model == 'article':
            target = Article.objects.get(pk=pk)
        elif model == 'story':
            target = Story.objects.get(pk=pk)
        elif model == 'document':
            target = SupportDocuement.objects.get(pk=pk)
        elif model == 'visual':
            target = Visual.objects.get(pk=pk)
        elif model == 'gallery':
            target = Gallery.objects.get(pk=pk)
        elif model == 'track':
            target = Track.objects.get(pk=pk)
        elif model == 'album':
            target = Album.objects.get(pk=pk)
        else:
            target = None
        return target
        
    def get_form_kwargs(self):
        kwargs = super(ResponsePostCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = self.get_target()
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Response"
        context['meta_desc'] = "Submit a response to \"{}\".".format(
                str(target),
            )
        return context

    def form_valid(self, form):
        member = self.request.user
        if self.kwargs['model'] == 'post':
            form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        if self.kwargs['members_only']:
            form.instance.members_only = self.kwargs['members_only']
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = Text.slugify_unique(self.model, form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'posts:response_detail',
                kwargs={'slug': self.object.slug},
            )

class ResponsePostListView(ListView):

    model = ResponsePost
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'responses'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return ResponsePost.objects.filter(
                Q(is_public=True)
            ).order_by(
                '-publication_date',
            )
        else:
            return ResponsePost.objects.filter(
                Q(is_public=True) | Q(members_only=False),
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Responses"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "Recent responses to content on {}.".format(
            profile.title,
        )
        return context
    
class TopResponsePostListView(ListView):

    model = ResponsePost
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'responses'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return ResponsePost.objects.filter(
                Q(is_public=True),
            ).order_by(
                '-weight',
                '-publication_date',
            )
        else:
            return ResponsePost.objects.filter(
                Q(is_public=True) | Q(members_only=False)
            ).order_by(
                '-weight',
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Responses"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "The best responses to content on {}.".format(
            profile.title,
        )
        return context

class MemberResponsePostView(ListView):

    model = ResponsePost
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'responses'

    def get_queryset(self, *args, **kwargs):
        member = self.request.user
        if self.request.user.is_authenticated:
            return ResponsePost.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else: 
            return ResponsePost.objects.filter(
                owner=member,
                members_only=False,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Responses by {}".format(member)
        context['meta_title'] = "Responses by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Responses by {} on {}.".format(
            member,
            profile.title,
        )
        return context

class ResponsePostDetailView(DetailView):

    model = ResponsePost
    context_object_name = 'response'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class ResponsePostUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'posts.change_responsepost'
    model = ResponsePost
    form_class = ResponsePostForm

    def get_target(self):
        if self.object.post:
            target = self.object.post
        elif self.object.article:
            target = self.object.article
        elif self.object.story:
            target = self.object.story
        elif self.object.document:
            target = self.object.document
        elif self.object.visual:
            target = self.object.visual
        elif self.object.gallery:
            target = self.object.gallery
        elif self.object.track:
            target = self.object.track
        elif self.object.album:
            target = self.object.album
        else:
            target = None
        return target

    def get_form_kwargs(self):
        kwargs = super(ResponsePostUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        target = self.get_target()
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        
        context['meta_desc'] = "Make changes to your response to \"{}\".".format(
            target,
        )
        return context

    def form_valid(self, form):
        form.instance.last_modified = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'posts:response_detail',
                kwargs={'slug': self.object.slug},
            )

class ResponsePostDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = ResponsePost

    def get_success_url(self):
        return reverse('members:studio')

def publish_responsepost_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(ResponsePost, pk=pk)
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
                    'posts:response_detail',
                    kwargs={
                        'slug': instance.slug,
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
                'posts:responsepost_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

def add_marshmallow_to_responsepost_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(ResponsePost, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=ResponsePost)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    ResponsePost.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('posts:member_responses', kwargs={'member': instance.owner.username}))

class ReportPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'posts:add_reportpost'
    model = ReportPost
    form_class = ReportPostForm

    def get_form_kwargs(self):
        kwargs = super(ReportPostCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Report"
        context['meta_desc'] = """Submit a new report."""
        return context

    def form_valid(self, form):
        member = self.request.user
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = Text.slugify_unique(self.model, form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('home:index',)

class ReportPostListView(ListView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = 'posts:delete_reportpost'
    model = ReportPost
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'reports'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return ReportPost.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return ReportPost.objects.filter(
                is_public=True,
                members_only=False,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Responses"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "Recent reports by {} contributors.".format(
            profile.title,
        )
    
class MemberReportPostView(ListView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = 'posts:delete_reportpost'
    model = ReportPost
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'reports'

    def get_queryset(self, *args, **kwargs):
        member = self.request.user
        if self.request.user.is_authenticated:
            return ReportPost.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else: 
            return ReportPost.objects.filter(
                owner=member,
                members_only=False,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Report Posts"
        context['meta_title'] = "Report Posts by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Report Posts by {} on {}.".format(
            member,
            profile.title,
        )
        return context

class ReportPostDetailView(DetailView, LoginRequiredMixin, PermissionRequiredMixin):

    permission_required = 'posts:delete_reportpost'
    model = ReportPost
    context_object_name = 'report'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = PostsAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile

class ReportPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = 'posts:add_deletepost'
    model = ReportPost

    def get_success_url(self):
        return reverse('members:studio')
