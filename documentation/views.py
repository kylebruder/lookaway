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
from django.utils import timezone, text
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from objects.utils import Text
from .forms import ArticleForm, ArticleSectionForm, DocumentationAppProfileForm, DocumentationPageSectionForm, StoryForm, StorySectionForm, SupportDocumentForm, SupportDocSectionForm
from .models import Article, ArticleSection, DocumentationAppProfile, DocumentationPageSection, Story, StorySection, SupportDocument, SupportDocSection

# Create your views here.

# Documentation App Profile Form
class DocumentationAppProfileUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):

    permission_required = 'documentation.change_documentationappprofile'
    model = DocumentationAppProfile
    form_class = DocumentationAppProfileForm

    def get_form_kwargs(self):
        kwargs = super(DocumentationAppProfileUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = "Update \"{}\" profile settings".format(profile.title)
        context['sections'] = DocumentationPageSection.objects.all().order_by(
            'order',
        )
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('documentation:documentation_page')

# Documentation Landing Page
class DocumentationPageView(TemplateView):

    template_name = 'documentation/documentation_page.html'

    def calculate_document_list_length(self, n):
        return round(math.ceil((n/1.5)/2) * 2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        context['sections'] = DocumentationPageSection.objects.filter(
            is_enabled = True,
        ).order_by(
            'order',
        )
        # Number of items to show in each list
        n = 3
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
            )[:n]
            # Exclude any Article that appears in the new articles list
            # from the top Article list.
            context['top_articles'] = public_articles.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_article_date,
            )[:n]
        # If there are less than 5 Articles,
        # include all of them in the new Article list.
        else:
            context['new_articles'] = public_articles.order_by(
                '-publication_date',
            )
        # Stories
        if self.request.user.is_authenticated:
            public_stories = Story.objects.filter(is_public=True)
        # Do not send member only Stories to non members
        else:
            public_stories = Story.objects.filter(
                is_public=True,
            )
        if public_stories.count() >= n:
            # Get the date of the nth newest Story
            # if there are n or more Stories
            last_new_story_date = public_stories.order_by(
                '-publication_date',
            )[n-1].publication_date
            context['new_stories'] = public_stories.order_by(
                '-publication_date',
            )[:n]
            # Exclude any Story that appears in the new releases list
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
        # SupportDocuments
        if self.request.user.is_authenticated:
            public_documents = SupportDocument.objects.filter(is_public=True)
        # Do not send member only Documents to non members
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
            # Exclude any Document that appears in the new releases list
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

# Documentation Page Section Views
class DocumentationPageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = 'documentation.add_documentationpagesection'
    model = DocumentationPageSection
    form_class = DocumentationPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(DocumentationPageSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Page Section"
        context['meta_desc'] = "Add a section to the {} landing page.".format(profile.title)
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
                'documentation:documentation_page_section_detail',
                kwargs={'slug': self.object.slug},
            )

class DocumentationPageSectionDetailView(LoginRequiredMixin, DetailView):

    model = DocumentationPageSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = profile.title
        return context

class DocumentationPageSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'documentation.change_documentationpagesection'
    model = DocumentationPageSection
    form_class = DocumentationPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(DocumentationPageSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
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
                'documentation:documentation_page_section_detail',
                kwargs={'pk': self.object.pk},
            )

class DocumentationPageSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):

    permission_required = 'documentation.delete_documentationpagesection'
    model = DocumentationPageSection
    context_object_name = "section"

    def get_success_url(self):
        return reverse(
            'documentation:documentation_page',
        )

# Article Views
class ArticleCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = Article
    form_class = ArticleForm

    def get_form_kwargs(self):
        kwargs = super(ArticleCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Article"
        context['meta_desc'] = """Create a new article. Once the article is \
            created, you can add sections containing the main content of \
            the article. Don't forget to publish the article once it is \
            ready."""
        return context

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
                'documentation:article_detail',
                kwargs={'slug': self.object.slug},
            )

class ArticleListView(ListView):

    model = Article
    paginate_by = 6
    context_object_name = 'articles'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Article.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Article.objects.filter(
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Articles"
        # SEO stuff
        context['meta_title'] = "{} | {}".format(
            context['app_list_context'],
            profile.title,
        )
        context['meta_desc'] = "Recently published articles by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:article_create',
            )
        return context   

class TopArticleListView(ListView):

    model = Article
    paginate_by = 6
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
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Articles"
        # SEO stuff
        context['meta_title'] = "Top Articles | {}".format(
            profile.title,
            )
        context['meta_desc'] = "The all time greatest {} articles.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:article_create',
            )
        return context   

class MemberArticleView(ListView):

    model = Article
    paginate_by = 6
    context_object_name = 'articles'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return Article.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else:
            return Article.objects.filter(
                owner=member,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Articles"
        # SEO stuff
        context['meta_title'] = "Articles by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Articles written by {} for {}.".format(
            member,
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:article_create',
            )
        context['member'] = member
        return context

class ArticleDetailView(DetailView):

    model = Article
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this article.".format(self.object.title)
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
                'documentation:article_detail',
                kwargs={'slug': self.object.slug},
            )

class ArticleDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Article

    def get_success_url(self):
        return reverse(
            'documentation:member_articles',
            kwargs={'member': self.request.user.username},
         )

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
    return HttpResponseRedirect(reverse('documentation:top_articles'))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Article Section"
        context['meta_desc'] = """Create a new article section. Once created, \
            article sections will instantly appear in the article selected in \
            the order chosen."""
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
                'documentation:article_section_detail',
                kwargs={'pk': self.object.pk},
            )

class ArticleSectionDetailView(LoginRequiredMixin, DetailView):

    model = ArticleSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        return context

class ArticleSectionUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = ArticleSection
    form_class = ArticleSectionForm

    def get_form_kwargs(self):
        kwargs = super(ArticleSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(
            self.object.title,
        )
        context['meta_desc'] = "Make changes to this article section from \"{}\".".format(
            self.object.article.title,
        )
        return context

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
    success_url = "/documentation/articles/{article_id}/"

    def post(self, request, *args, **kwargs):
        instance = self.model.objects.get(pk=kwargs['pk'])
        if self.request.POST and self.request.user.pk == instance.owner.pk:
            instance.delete()                
            messages.add_message(
                request, messages.INFO,
                'The {} "{}" has been successfully deleted.'.format(
                    self.model.__name__,
                    instance,
                )
            )
            return HttpResponseRedirect(
                reverse(
                    'documentation:article_detail',
                    kwargs={'slug': instance.article.slug},
                )
            )
    
        else:
            messages.add_message(
                request, messages.ERROR,
                'You do not own "{}". Delete Failed. It is not nice to delete \
                other people\'s work!'.format(instance)
            )
            return HttpResponseRedirect(
                reverse('home:index')
            )

# Support Document Views
class SupportDocumentCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = SupportDocument
    form_class = SupportDocumentForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocumentCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Document"
        context['meta_desc'] = """Create a new document. Once the document is \
            created, you can add sections containing the main content of \
            the document. Don't forget to publish the document once it is \
            ready."""
        return context

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
                'documentation:support_document_detail',
                kwargs={'slug': self.object.slug},
            )

class SupportDocumentListView(ListView):

    model = SupportDocument
    paginate_by = 6
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return SupportDocument.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True),
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return SupportDocument.objects.filter(
                is_public=True,
            ).order_by(
                '-publication_date',
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Information"
        # SEO stuff
        context['meta_title'] = "New Information | {}".format(
            profile.title,
            )
        context['meta_desc'] = "Recently published documentation by {} staff contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:support_document_create',
            )
        return context   

class TopSupportDocumentListView(ListView):

    model = SupportDocument
    paginate_by = 6
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
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Information"
        # SEO stuff
        context['meta_title'] = "Top Information | {}".format(
            profile.title,
            )
        context['meta_desc'] = "Important information documented by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:support_document_create',
            )
        return context

class MemberSupportDocumentView(ListView):

    model = SupportDocument
    paginate_by = 6
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return SupportDocument.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else:
            return SupportDocument.objects.filter(
                owner=member,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Information"
        # SEO stuff
        context['meta_title'] = "Information by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Information documented by {} for {}.".format(
            member,
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:support_document_create',
            )
        context['member'] = member
        return context

class SupportDocumentDetailView(DetailView):

    model = SupportDocument
    context_object_name = 'document'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        sections = SupportDocSection.objects.filter(support_reference=self.object.pk)
        context['refs'] = {}
        for s in sections:
            if s.support_document not in context['refs']:
                context['refs'][s.support_document] = s.pk
        print(context['refs'])
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this document.".format(self.object.title)
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
                'documentation:support_document_detail',
                kwargs={'slug': self.object.slug},
            )

class SupportDocumentDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = SupportDocument

    def get_success_url(self):
        return reverse(
            'documentation:member_support_documents',
            kwargs={'member': self.request.user.username},
         )

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
    return HttpResponseRedirect(reverse('documentation:top_support_documents'))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Document Section"
        context['meta_desc'] = """Create a new document section. Once created, \
            document sections will instantly appear in the document selected in \
            the order chosen."""
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
                'documentation:support_doc_section_detail',
                kwargs={'pk': self.object.pk},
            )

class SupportDocSectionDetailView(LoginRequiredMixin, DetailView):

    model = SupportDocSection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        return context

class SupportDocSectionUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = SupportDocSection
    form_class = SupportDocSectionForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(
            self.object.title,
        )
        context['meta_desc'] = "Make changes to this document section from \"{}\".".format(
            self.object.support_document.title,
        )
        return context

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

    def post(self, request, *args, **kwargs):
        instance = self.model.objects.get(pk=kwargs['pk'])
        if self.request.POST and self.request.user.pk == instance.owner.pk:
            instance.delete()
            messages.add_message(
                request, messages.INFO,
                'The {} "{}" has been successfully deleted.'.format(
                    self.model.__name__,
                    instance,
                )
            )
            return HttpResponseRedirect(
                reverse(
                    'documentation:support_document_detail',
                    kwargs={'slug': instance.support_document.slug},
                )
            )

        else:
            messages.add_message(
                request, messages.ERROR,
                'You do not own "{}". Delete Failed. It is not nice to delete \
                other people\'s work!'.format(instance)
            )
            return HttpResponseRedirect(
                reverse('home:index')
            )

# Story Views
class StoryCreateView(LoginRequiredMixin, MemberCreateMixin, CreateView):

    model = Story
    form_class = StoryForm

    def get_form_kwargs(self):
        kwargs = super(StoryCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Story"
        context['meta_desc'] = """Create a new story. Once the story is \
            created, you can add sections containing the main content of \
            the story. Don't forget to publish the story once it is \
            ready."""
        return context

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
                'documentation:story_detail',
                kwargs={'slug': self.object.slug},
            )

class StoryListView(ListView):

    model = Story
    paginate_by = 6
    context_object_name = 'stories'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Story.objects.filter(
                Q(owner=self.request.user) | Q(is_public=True)
            ).order_by(
                'is_public',
                '-publication_date',
            )
        else:
            return Story.objects.filter(
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "New Stories"
        # SEO stuff
        context['meta_title'] = "New Stories | {}".format(
            profile.title,
        )
        context['meta_desc'] = "Recent stories written by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:story_create',
            )
        return context   

class TopStoryListView(ListView):

    model = Story
    paginate_by = 6
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
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Top Stories"
        # SEO stuff
        context['meta_title'] = "Top Stories | {}".format(
            profile.title,
        )
        context['meta_desc'] = "Excellent stories written by {} contributors.".format(
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:story_create',
            )
        return context

class MemberStoryView(ListView):

    model = Story
    paginate_by = 6
    context_object_name = 'stories'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        if self.request.user.pk == member.pk:
            return Story.objects.filter(
                owner=member
            ).order_by(
                '-last_modified',
            )
        else:
            return Story.objects.filter(
                owner=member,
                is_public=True,
            ).order_by(
                '-publication_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['app_list_context'] = "Stories"
        context['meta_title'] = "Stories by {} | {}".format(
            member,
            profile.title,
            )
        context['meta_desc'] = "Stories published by {} for {}.".format(
            member,
            profile.title,
        )
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:story_create',
            )
        context['member'] = member
        return context

class StoryDetailView(DetailView):

    model = Story
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(self.object.title)
        context['meta_desc'] = "Make changes to this story.".format(self.object.title)
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
                'documentation:story_detail',
                kwargs={'slug': self.object.slug},
            )

class StoryDeleteView(LoginRequiredMixin, MemberDeleteMixin, DeleteView):

    model = Story

    def get_success_url(self):
        return reverse(
            'documentation:member_stories',
            kwargs={'member': self.request.user.username},
         )

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
    return HttpResponseRedirect(reverse('documentation:top_stories'))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "New Story Section"
        context['meta_desc'] = """Create a new story section. Once created, \
            story sections will instantly appear in the story selected in \
            the order chosen."""
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
                'documentation:story_section_detail',
                kwargs={'pk': self.object.pk},
            )

class StorySectionDetailView(LoginRequiredMixin, DetailView):

    model = StorySection
    context_object_name = 'section'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        return context

class StorySectionUpdateView(LoginRequiredMixin, MemberUpdateMixin, UpdateView):

    model = StorySection
    form_class = StorySectionForm

    def get_form_kwargs(self):
        kwargs = super(StorySectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['meta_title'] = "Update \"{}\"".format(
            self.object.title,
        )
        context['meta_desc'] = "Make changes to this story section from \"{}\".".format(
            self.object.story.title,
        )
        return context

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

    def post(self, request, *args, **kwargs):
        instance = self.model.objects.get(pk=kwargs['pk'])
        if self.request.POST and self.request.user.pk == instance.owner.pk:
            instance.delete()
            messages.add_message(
                request, messages.INFO,
                'The {} "{}" has been successfully deleted.'.format(
                    self.model.__name__,
                    instance,
                )
            )
            return HttpResponseRedirect(
                reverse(
                    'documentation:story_detail',
                    kwargs={'slug': instance.story.slug},
                )
            )

        else:
            messages.add_message(
                request, messages.ERROR,
                'You do not own "{}". Delete Failed. It is not nice to delete \
                other people\'s work!'.format(instance)
            )
            return HttpResponseRedirect(
                reverse('home:index')
            )
