from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    )
from django.http import HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.utils import timezone, text
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from .forms import ArticleForm, ArticleSectionForm, StoryForm, StorySectionForm, SupportDocumentForm, SupportDocSectionForm
from .models import Article, ArticleSection, Story, StorySection, SupportDocument, SupportDocSection

# Create your views here.

# Documentation Landing Page
class DocumentationPageView(TemplateView):

    template_name = 'documentation/documentation_page.html'

    def calculate_document_list_length(self, n):
        return round(math.ceil((n/1.5)/2) * 2)

    def get_context_data(self, **kwargs):
        # Number of items to show in each list
        n = 5
        context = super().get_context_data(**kwargs)
        # Articles
        public_articles = Article.objects.filter(is_public=True)
        if public_articles.count() >= n:
            # Get the date of the 5th newest Article
            # if there are 5 or more Articles.
            last_new_article_date = public_articles.order_by(
                '-publication_date',
            )[n-1].publication_date
            # Get the 5 newest Articles.
            context['new_articles'] = public_articles.order_by(
                '-publication_date',
            )[:self.calculate_article_list_length(n)]
            # Exclude any Article that appears in the new articles list
            # from the top Article list.
            context['top_articles'] = public_articles.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_article_date,
            )[:self.calculate_article_list_length(n)]
        # If there are less than 5 Articles,
        # include all of them in the new Article list.
        else:
            context['new_articles'] = public_articles.order_by(
                '-publication_date',
            )
        # Stories
        if self.request.user.is_authenticated:
            public_stories = Story.objects.filter(is_public=True)
        # Do not send member only Articles to non members
        else:
            public_stories = Story.objects.filter(
                is_public=True,
            )
        if public_stories.count() >= n:
            # Get the date of the nth newest Story
            # if there are n or more Storys
            last_new_story_date = public_stories.order_by(
                '-publication_date',
            )[n-1].publication_date
            context['new_stories'] = public_stories.order_by(
                '-publication_date',
            )[:n]
            # Exclude any Article that appears in the new releases list
            # from the top Story list
            context['top_stories'] = public_stories.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_story_date,
            )[:n]
        else:
            context['new_stories'] = public_stories.order_by(
                '-publication_date',
            )[:n]
        # Documents
        if self.request.user.is_authenticated:
            public_documents = SupportDocument.objects.filter(is_public=True)
        # Do not send member only Articles to non members
        else:
            public_documents = SupportDocument.objects.filter(
                is_public=True,
            )
        if public_documents.count() >= n:
            # Get the date of the nth newest Document
            # if there are n or more Documents
            last_new_document_date = public_documents.order_by(
                '-publication_date',
            )[n-1].publication_date
            context['new_documents'] = public_documents.order_by(
                '-publication_date',
            )[:n]
            # Exclude any Article that appears in the new releases list
            # from the top Document list
            context['top_documents'] = public_documents.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_document_date,
            )[:n]
        else:
            context['new_documents'] = public_documents.order_by(
                '-publication_date',
            )[:n]
        return context
# Support Article Views

class ArticleCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = Article
    form_class = ArticleForm

    def get_form_kwargs(self):
        kwargs = super(ArticleCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = text.slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'documentation:article_detail',
                kwargs={'slug': self.object.slug},
            )

class ArticleListView(ListView):

    model = Article
    paginate_by = 5
    context_object_name = 'articles'

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context   

class TopArticleListView(ListView):

    model = Article
    paginate_by = 5
    context_object_name = 'articles'

    def get_queryset(self, *args, **kwargs):
        return Article.objects.filter(
                is_public=True,
            ).order_by(
                '-weight',
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context   

class MemberArticleView(LoginRequiredMixin, ListView):

    model = Article
    paginate_by = 5
    context_object_name = 'articles'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Article.objects.filter(
            owner=member
        ).order_by(
            'is_public', 
            '-creation_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class ArticleDetailView(DetailView):

    model = Article
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        context['sections'] = ArticleSection.objects.filter(
            article=self.get_object(),
        ).order_by('order')
        return context

class ArticleUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Article
    form_class = ArticleForm

    def get_form_kwargs(self):
        kwargs = super(ArticleUpdateView, self).get_form_kwargs()
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
                'documentation:article_detail',
                kwargs={'slug': self.object.slug},
            )

class ArticleDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Article

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_article_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Article, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Article)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Article.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('documentation:public_articles'))

def publish_article_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Article, pk=pk)
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
                    'documentation:article_detail',
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
                'documentation:article_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# ArticleSection Views

class ArticleSectionCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = ArticleSection
    form_class = ArticleSectionForm

    def get_form_kwargs(self):
        kwargs = super(ArticleSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['article'] = self.request.GET.get('article')
        return kwargs

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
                'documentation:article_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MemberArticleSectionView(LoginRequiredMixin, ListView):

    model = ArticleSection
    paginate_by = 5
    context_object_name = 'sections'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return ArticleSection.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class ArticleSectionDetailView(LoginRequiredMixin, DetailView):

    model = ArticleSection
    context_object_name = 'section'

class ArticleSectionUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = ArticleSection
    form_class = ArticleSectionForm

    def get_form_kwargs(self):
        kwargs = super(ArticleSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Update last modified date for the ArticleSection
        form.instance.last_modified = timezone.now()
        # Update last modified date for the parent Article too
        print(Article.objects.get(
            pk=form.instance.article.pk
        ) )
        s = Article.objects.get(
            pk=form.instance.article.pk
        )
        s.last_modified = timezone.now()
        s.save()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'documentation:article_section_detail',
                kwargs={'pk': self.object.pk},
            )

class ArticleSectionDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = ArticleSection

    def get_success_url(self):
        return reverse('members:studio')

# Support Document Views

class SupportDocumentCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = SupportDocument
    form_class = SupportDocumentForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocumentCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = text.slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'documentation:support_document_detail',
                kwargs={'slug': self.object.slug},
            )

class SupportDocumentListView(ListView):

    model = SupportDocument
    paginate_by = 5
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        return SupportDocument.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context   

class TopSupportDocumentListView(ListView):

    model = SupportDocument
    paginate_by = 5
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        return SupportDocument.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context

class MemberSupportDocumentView(LoginRequiredMixin, ListView):

    model = SupportDocument
    paginate_by = 5
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return SupportDocument.objects.filter(
            owner=member
        ).order_by(
            'is_public', 
            '-creation_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class SupportDocumentDetailView(DetailView):

    model = SupportDocument
    context_object_name = 'document'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        sections = SupportDocSection.objects.filter(support_reference=self.object.pk)
        context['refs'] = ()
        for s in sections:
            if s.support_document not in context['refs']:
                context['refs'] += (s.support_document,)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        context['sections'] = SupportDocSection.objects.filter(
            support_document=self.get_object(),
        ).order_by('order')
        return context

class SupportDocumentUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = SupportDocument
    form_class = SupportDocumentForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocumentUpdateView, self).get_form_kwargs()
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
                'documentation:support_document_detail',
                kwargs={'slug': self.object.slug},
            )

class SupportDocumentDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = SupportDocument

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_support_document_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(SupportDocument, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=SupportDocument)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    SupportDocument.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('documentation:public_support_documents'))

def publish_support_document_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(SupportDocument, pk=pk)
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
                    'documentation:support_document_detail',
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
                'documentation:support_document_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# SupportDocSection Views

class SupportDocSectionCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = SupportDocSection
    form_class = SupportDocSectionForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['support_document'] = self.request.GET.get('support_document')
        return kwargs

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
                'documentation:support_doc_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MemberSupportDocSectionView(LoginRequiredMixin, ListView):

    model = SupportDocSection
    paginate_by = 5
    context_object_name = 'sections'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return SupportDocSection.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class SupportDocSectionDetailView(LoginRequiredMixin, DetailView):

    model = SupportDocSection
    context_object_name = 'section'

class SupportDocSectionUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = SupportDocSection
    form_class = SupportDocSectionForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Update last modified date for the SupportDocSection
        form.instance.last_modified = timezone.now()
        # Update last modified date for the parent SupportDocument too
        print(SupportDocument.objects.get(
            pk=form.instance.support_document.pk
        ) )
        s = SupportDocument.objects.get(
            pk=form.instance.support_document.pk
        )
        s.last_modified = timezone.now()
        s.save()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'documentation:support_doc_section_detail',
                kwargs={'pk': self.object.pk},
            )

class SupportDocSectionDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = SupportDocSection

    def get_success_url(self):
        return reverse('members:studio')

# Story Views

class StoryCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = Story
    form_class = StoryForm

    def get_form_kwargs(self):
        kwargs = super(StoryCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        member = Member.objects.get(pk=self.request.user.pk)
        form.instance.creation_date = timezone.now()
        form.instance.owner = member
        form.instance.slug = text.slugify(form.instance.title)
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'documentation:story_detail',
                kwargs={'slug': self.object.slug},
            )

class StoryListView(ListView):

    model = Story
    paginate_by = 5
    context_object_name = 'stories'

    def get_queryset(self, *args, **kwargs):
        return Story.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context   

class TopStoryListView(ListView):

    model = Story
    paginate_by = 5
    context_object_name = 'stories'

    def get_queryset(self, *args, **kwargs):
        return Story.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-publication_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context

class MemberStoryView(LoginRequiredMixin, ListView):

    model = Story
    paginate_by = 5
    context_object_name = 'stories'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Story.objects.filter(
            owner=member
        ).order_by(
            'is_public',
            '-creation_date',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class StoryDetailView(DetailView):

    model = Story
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        context['sections'] = StorySection.objects.filter(
            story=self.get_object(),
        ).order_by('order')
        return context

class StoryUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = Story
    form_class = StoryForm

    def get_form_kwargs(self):
        kwargs = super(StoryUpdateView, self).get_form_kwargs()
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
                'documentation:story_detail',
                kwargs={'slug': self.object.slug},
            )

class StoryDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Story

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_story_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Story, pk=pk)
    if instance.is_public:
        successful, weight, amount = member.allocate_marshmallow(instance, model=Story)
        if successful:
            messages.add_message(
                request, messages.INFO,
                'You gave {} to the {} "{}"'.format(
                    amount,
                    Story.__name__,
                    instance,
                )
           )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'You are not allowed to give marshmallows at this time'
            )
    return HttpResponseRedirect(reverse('documentation:public_stories'))

def publish_story_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Story, pk=pk)
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
                    'documentation:story_detail',
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
                'documentation:story_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# StorySection Views

class StorySectionCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = StorySection
    form_class = StorySectionForm

    def get_form_kwargs(self):
        kwargs = super(StorySectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['story'] = self.request.GET.get('story')
        return kwargs

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
                'documentation:story_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MemberStorySectionView(LoginRequiredMixin, ListView):

    model = StorySection
    paginate_by = 5
    context_object_name = 'sections'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return StorySection.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class StorySectionDetailView(LoginRequiredMixin, DetailView):

    model = StorySection
    context_object_name = 'section'

class StorySectionUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = StorySection
    form_class = StorySectionForm

    def get_form_kwargs(self):
        kwargs = super(StorySectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Update last modified date for the StorySection
        form.instance.last_modified = timezone.now()
        # Update last modified date for the parent Story too
        print(Story.objects.get(
            pk=form.instance.story.pk
        ) )
        s = Story.objects.get(
            pk=form.instance.story.pk
        )
        s.last_modified = timezone.now()
        s.save()
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse(
                'documentation:story_section_detail',
                kwargs={'pk': self.object.pk},
            )

class StorySectionDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = StorySection

    def get_success_url(self):
        return reverse('documentation:story_detail',
            kwargs={'slug': self.object.story.slug},
        )
