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
from objects.utils import Text
from .forms import PostsAppProfileForm, PostsPageSectionForm, PostForm
from .models import PostsAppProfile, PostsPageSection, Post

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
        context['sections'] = PostsPageSection.objects.filter(
            is_enabled = True,
        ).order_by(
            'order',
        )
        # New and top Post instances
        context['new_posts'], context['top_posts'] = self.get_sets(
            Posts,
            profile.n_posts,
            show_new=profile.show_new_posts,
            show_top=profile.show_top_posts,
        )
        # New and top Response instances
        context['new_responses'], context['top_responses'] = self.get_sets(
            Bar,
            profile.n_responses,
            show_new=profile.show_new_responses,
            show_top=profile.show_top_responses,
        )
        # Create Posts button
        if self.request.user.has_perm('posts.add_posts'):
            context['show_create_posts_button'] = True
            context['create_posts_url'] = reverse(
                'posts:posts_create',
            )
        # Create Bar button
        if self.request.user.has_perm('posts.add_response'):
            context['show_create_response_button'] = True
            context['create_response_url'] = reverse(
                'posts:response_create',
            )
        # Update AppProfile button
        if self.request.user.has_perm('posts.change_postsappprofile'):
            context['show_edit_profile_button'] = True
            context['edit_profile_url'] = reverse(
                'posts:posts_app_profile_update',
                kwargs={'pk': 1},
            )
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

class PostCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'posts:add_post'
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
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Post.objects.filter(
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
    
class PostResponseListView(ListView):

    model = Post
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).exclude(re=None).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Post.objects.filter(
                is_public=True,
                members_only=False,
            ).exclude(re=None).order_by(
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
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-weight',
                '-publication_date',
            )
        else:
            return Post.objects.filter(
                is_public=True,
                members_only=False,
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

class TopPostResponseListView(ListView):

    model = Post
    paginate_by = PostsAppProfile.objects.get_or_create(pk=1)[0].response_list_pagination
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).exclude(re=None).order_by(
                'is_public',
                '-weight',
                '-publication_date',
            )
        else:
            return Post.objects.filter(
                is_public=True,
                members_only=False,
            ).exclude(re=None).order_by(
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
        context['meta_desc'] = "The best responses by {} contributors.".format(
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
        profile, created = FooAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        # Get the posts that are a response to this post
        context['responses'] = Post.objects.filter(
            re=self.object,
        ).filter(
            is_public=True,
        ).order_by('weight', '-publication_date')
        # Check if any responses can be seen by non-members
        for re in context['responses']:
            if not re.members_only:
                context['public_response'] = True
        return context

class PostUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

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

class PostDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

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
                'members:post_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

