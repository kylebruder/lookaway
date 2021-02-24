from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from objects.utils import Text
from .forms import PostForm
from .models import Post

# Create your views here.

class PostCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = Post
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super(PostCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
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
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                is_public=True,
            ).order_by(
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
        context['new'] = True
        return context
    
class TopPostListView(ListView):

    model = Post
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-publication_date',
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context
    
class MemberPostView(ListView):

    model = Post
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
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
        context['user_only'] = True
        context['member'] = member
        return context

class PostDetailView(DetailView):

    model = Post
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

    model = Post
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super(PostUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

