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
from lookaway.mixins import AppPageMixin
from members.models import Member
from members.mixins import MemberCreateMixin, MemberUpdateMixin, MemberDeleteMixin
from objects.utils import Text
from posts.models import ResponsePost
from .app_profile_mixins import NewModelListMixin, TopModelListMixin, StudioListMixin, ModelByMemberMixin
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
        # Add documentation page section button
        if self.request.user.has_perm('documentation.add_documentationpagesection'):
            context['show_documentation_page_section_add_button'] = True
            context['documentation_page_section_add_button'] = {
                'url': reverse(
                    'documentation:documentation_page_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_documentationpagesection'):
            context['show_documentation_page_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_documentationpagesection'):
            context['show_documentation_page_section_delete_button'] = True
        return context

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse('documentation:documentation_page')

# Documentation Landing Page
class DocumentationPageView(TemplateView, AppPageMixin):

    template_name = 'documentation/documentation_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        # SEO stuff
        context['meta_title'] = profile.title
        context['meta_desc'] = profile.meta_description
        # Sections
        sections = DocumentationPageSection.objects.filter(
            is_enabled = True,
        ).order_by(
            'order',
        )
        # Create Article button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_article_add_button'] = True
            context['article_add_button'] = {
                'url': reverse('documentation:article_create'),
                'text': "+Article",
            }
        # Create Story button
        if self.request.user.has_perm('documentation.add_story'):
            context['show_story_add_button'] = True
            context['story_add_button'] = {
                'url': reverse('documentation:story_create'),
                'text': "+Story",
            }
        # Create Document button
        if self.request.user.has_perm('documentation.add_supportdocument'):
            context['show_document_add_button'] = True
            context['document_add_button'] = {
                'url': reverse('documentation:support_document_create'),
                'text': "+Info",
            }
        # Update AppProfile button
        if self.request.user.has_perm('documentation.change_documentationappprofile'):
            context['show_profile_edit_button'] = True
            context['profile_edit_button'] = {
                'url': reverse('documentation:documentation_app_profile_update',
                    kwargs={'pk': 1},
                ),
                'text': "Edit App"
            }
        # Add documentation page section button
        if self.request.user.has_perm('documentation.add_documentationpagesection'):
            context['show_section_add_button'] = True
            context['section_add_button'] = {
                'url': reverse(
                    'documentation:documentation_page_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_documentationpagesection'):
            context['show_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_documentationpagesection'):
            context['show_section_delete_button'] = True
        if self.request.user.is_authenticated:
            context['sections'] = sections
        else:
            context['sections'] = sections.exclude(
                members_only=True
            )
        # Articles
        context['new_articles'], context['top_articles'] = self.get_sets(
            Article,
            profile.n,
            show_new=profile.show_new_articles,
            show_top=profile.show_top_articles,
        )
        # Stories
        context['new_stories'], context['top_stories'] = self.get_sets(
            Story,
            profile.n,
            show_new=profile.show_new_stories,
            show_top=profile.show_top_stories,
        )
        # SupportDocuments
        context['new_documents'], context['top_documents'] = self.get_sets(
            SupportDocument,
            profile.n,
            show_new=profile.show_new_support_documents,
            show_top=profile.show_top_support_documents,
        )
        return context

# Documentation Page Section Views
class DocumentationPageSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = 'documentation.add_documentationpagesection'
    model = DocumentationPageSection
    form_class = DocumentationPageSectionForm

    def get_form_kwargs(self):
        kwargs = super(DocumentationPageSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['order'] = self.request.GET.get('order')
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
                kwargs={'pk': self.object.pk},
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
        # Add documentation page section button
        if self.request.user.has_perm('documentation.add_documentationpagesection'):
            context['show_documentation_page_section_add_button'] = True
            context['documentation_page_section_add_button'] = {
                'url': reverse(
                    'documentation:documentation_page_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_documentationpagesection'):
            context['show_documentation_page_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_documentationpagesection'):
            context['show_documentation_page_section_delete_button'] = True
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
class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'documentation.add_article'
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

class ArticleListView(NewModelListMixin, ListView):

    model = Article
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:article_create',
            )
        return context   

class TopArticleListView(TopModelListMixin, ListView):

    model = Article
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:article_create',
            )
        return context   

class MemberArticleView(ModelByMemberMixin, ListView):

    model = Article
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:article_create',
            )
        return context

class ArticleStudioListView(StudioListMixin, ListView):

    model = Article
    context_object_name = 'articles'
    template_name = 'documentation/studio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:article_create',
            )
        return context

class ArticleDetailView(DetailView):

    model = Article
    context_object_name = 'article'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['sections'] = ArticleSection.objects.filter(
            article=self.get_object(),
        ).order_by('order')
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            # Post Actions
            if self.object.owner.pk == member.pk:
                if not self.object.is_public:
                    context['show_publish_button'] = True
                    context['publish_button'] = {
                        'url': reverse(
                            'documentation:publish_article',
                            kwargs={
                                'pk': self.object.pk,
                            },
                        )
                    }
                context['show_edit_button'] = True
                context['edit_button'] = {
                     'url': reverse(
                        'documentation:article_update',
                        kwargs={
                            'slug': self.object.slug,
                        },
                    )
                }
                context['show_delete_button'] = True
                context['delete_button'] = {
                     'url': reverse(
                        'documentation:article_delete',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    )
                }
            # Marshmallow button
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
                context['marshmallow_button'] = {
                    'url': reverse(
                        'documentation:article_marshmallow',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    ),
                }
            # Response button
            if self.request.user.has_perm('posts.add_responsepost'):
                context['can_respond'] = True
                context['response_button'] = {
                    'url': reverse(
                        'posts:response_post_create',
                        kwargs={
                            'model': "article",
                            'pk': self.object.pk,
                            'members_only': False,
                        },
                    ),
                }
            # Get the posts that are a response to this article
            context['responses'] = ResponsePost.objects.filter(
                article=self.object,
                is_public=True,
            ).order_by('weight', '-publication_date')[:5]
        else:
            context['responses'] = ResponsePost.objects.filter(
                article=self.object,
                is_public=True,
                members_only=False,
            ).order_by('weight', '-publication_date')[:5]
        # Add section button
        if self.request.user.has_perm('documentation.add_articlesection'):
            context['show_section_add_button'] = True
            context['section_add_button'] = {
                'url': reverse(
                    'documentation:article_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_articlesection'):
            context['show_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_articlesection'):
            context['show_section_delete_button'] = True
        return context

class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'documentation.change_article'
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

class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'documentation.delete_article'
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
class ArticleSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'documentation.add_articlesection'
    model = ArticleSection
    form_class = ArticleSectionForm

    def get_form_kwargs(self):
        kwargs = super(ArticleSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['article'] = self.request.GET.get('article')
        kwargs['order'] = self.request.GET.get('order')
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
        # Add section button
        if self.request.user.has_perm('documentation.add_articlesection'):
            context['show_section_add_button'] = True
            context['section_add_button'] = {
                'url': reverse(
                    'documentation:article_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_articlesection'):
            context['show_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_articlesection'):
            context['show_section_delete_button'] = True
        return context

class ArticleSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'documentation.change_articlesection'
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

class ArticleSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'documentation.delete_articlesection'
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
class SupportDocumentCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'documentation.add_supportdocument'
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

class SupportDocumentListView(NewModelListMixin, ListView):

    model = SupportDocument
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:support_document_create',
            )
        return context   

class TopSupportDocumentListView(TopModelListMixin, ListView):

    model = SupportDocument
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:support_document_create',
            )
        return context

class MemberSupportDocumentView(ModelByMemberMixin, ListView):

    model = SupportDocument
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'documents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:support_document_create',
            )
        return context

class SupportDocumentStudioListView(StudioListMixin, ListView):

    model = SupportDocument
    context_object_name = 'document'
    template_name = 'documentation/studio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:support_document_create',
            )
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
        context['sections'] = SupportDocSection.objects.filter(
            support_document=self.get_object(),
        ).order_by('order')
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            # Post Actions
            if self.object.owner.pk == member.pk:
                if not self.object.is_public:
                    context['show_publish_button'] = True
                    context['publish_button'] = {
                        'url': reverse(
                            'documentation:publish_support_document',
                            kwargs={
                                'pk': self.object.pk,
                            },
                        )
                    }
                context['show_edit_button'] = True
                context['edit_button'] = {
                     'url': reverse(
                        'documentation:support_document_update',
                        kwargs={
                            'slug': self.object.slug,
                        },
                    )
                }
                context['show_delete_button'] = True
                context['delete_button'] = {
                     'url': reverse(
                        'documentation:support_document_delete',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    )
                }
            # Marshmallow button
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
                context['marshmallow_button'] = {
                    'url': reverse(
                        'documentation:support_document_marshmallow',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    ),
                }
            # Response button
            if self.request.user.has_perm('posts.add_responsepost'):
                context['can_respond'] = True
                context['response_button'] = {
                    'url': reverse(
                        'posts:response_post_create',
                        kwargs={
                            'model': "support_document",
                            'pk': self.object.pk,
                            'members_only': False,
                        },
                    ),
                }
            # Get the posts that are a response to this support_document
            context['responses'] = ResponsePost.objects.filter(
                document=self.object,
                is_public=True,
            ).order_by('weight', '-publication_date')[:5]
        else:
            context['responses'] = ResponsePost.objects.filter(
                document=self.object,
                is_public=True,
                members_only=False,
            ).order_by('weight', '-publication_date')[:5]
        # Add section button
        if self.request.user.has_perm('documentation.add_supportdocsection'):
            context['show_section_add_button'] = True
            context['section_add_button'] = {
                'url': reverse(
                    'documentation:support_doc_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_supportdocsection'):
            context['show_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_supportdocsection'):
            context['show_section_delete_button'] = True
        return context

class SupportDocumentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'documentation.change_supportdocument'
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

class SupportDocumentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'documentation.delete_supportdocument'
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
class SupportDocSectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'documentation.add_supportdocsection'
    model = SupportDocSection
    form_class = SupportDocSectionForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['support_document'] = self.request.GET.get('support_document')
        kwargs['order'] = self.request.GET.get('order')
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
        # Add section button
        if self.request.user.has_perm('documentation.add_supportdocsection'):
            context['show_section_add_button'] = True
            context['section_add_button'] = {
                'url': reverse(
                    'documentation:support_doc_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_supportdocsection'):
            context['show_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_supportdocsection'):
            context['show_section_delete_button'] = True
        return context

class SupportDocSectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'documentation.change_supportdocsection'
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

class SupportDocSectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'documentation.delete_supportdocsection'
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
class StoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'documentation.add_story'
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

class StoryListView(NewModelListMixin, ListView):

    model = Story
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'stories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:story_create',
            )
        return context   

class TopStoryListView(TopModelListMixin, ListView):

    model = Story
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'stories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:story_create',
            )
        return context

class MemberStoryView(ModelByMemberMixin, ListView):

    model = Story
    try:
        paginate_by = DocumentationAppProfile.objects.get_or_create(pk=1)[0].list_pagination
    except:
        paginate_by = 10
    context_object_name = 'stories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:story_create',
            )
        return context

class StoryStudioListView(StudioListMixin, ListView):

    model = Story
    template_name= 'documentation/studio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create button
        if self.request.user.has_perm('documentation.add_article'):
            context['show_create_button'] = True
            context['create_button_url'] = reverse(
                'documentation:story_create',
            )
        return context

class StoryDetailView(DetailView):

    model = Story
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # App profile
        profile, created = DocumentationAppProfile.objects.get_or_create(pk=1)
        context['profile'] = profile
        context['sections'] = StorySection.objects.filter(
            story=self.get_object(),
        ).order_by('order')
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            # Story Actions
            if self.object.owner.pk == member.pk:
                if not self.object.is_public:
                    context['show_publish_button'] = True
                    context['publish_button'] = {
                        'url': reverse(
                            'documentation:publish_story',
                            kwargs={
                                'pk': self.object.pk,
                            },
                        )
                    }
                context['show_edit_button'] = True
                context['edit_button'] = {
                     'url': reverse(
                        'documentation:story_update',
                        kwargs={
                            'slug': self.object.slug,
                        },
                    )
                }
                context['show_delete_button'] = True
                context['delete_button'] = {
                     'url': reverse(
                        'documentation:story_delete',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    )
                }
            # Marshmallow button
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
                context['marshmallow_button'] = {
                    'url': reverse(
                        'documentation:story_marshmallow',
                        kwargs={
                            'pk': self.object.pk,
                        },
                    ),
                }
            # Response button
            if self.request.user.has_perm('posts.add_responsepost'):
                context['can_respond'] = True
                context['response_button'] = {
                    'url': reverse(
                        'posts:response_post_create',
                        kwargs={
                            'model': "story",
                            'pk': self.object.pk,
                            'members_only': False,
                        },
                    ),
                }
            # Get the posts that are a response to this story
            context['responses'] = ResponsePost.objects.filter(
                story=self.object,
                is_public=True,
            ).order_by('weight', '-publication_date')[:5]
        else:
            context['responses'] = ResponsePost.objects.filter(
                story=self.object,
                is_public=True,
                members_only=False,
            ).order_by('weight', '-publication_date')[:5]
        # Add section button
        if self.request.user.has_perm('documentation.add_storysection'):
            context['show_section_add_button'] = True
            context['section_add_button'] = {
                'url': reverse(
                    'documentation:story_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_storysection'):
            context['show_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_storysection'):
            context['show_section_delete_button'] = True
        return context

class StoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'documentation.change_story'
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

class StoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'documentation.delete_story'
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
class StorySectionCreateView(LoginRequiredMixin, PermissionRequiredMixin, MemberCreateMixin, CreateView):

    permission_required = 'documentation.add_storysection'
    model = StorySection
    form_class = StorySectionForm

    def get_form_kwargs(self):
        kwargs = super(StorySectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['story'] = self.request.GET.get('story')
        kwargs['order'] = self.request.GET.get('order')
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
        # Add section button
        if self.request.user.has_perm('documentation.add_storysection'):
            context['show_section_add_button'] = True
            context['section_add_button'] = {
                'url': reverse(
                    'documentation:story_section_create',
                ),
            }
        # Edit documentation page section button
        if self.request.user.has_perm('documentation.change_storysection'):
            context['show_section_edit_button'] = True
        # Delete documentation page section button
        if self.request.user.has_perm('documentation.delete_storysection'):
            context['show_section_delete_button'] = True
        return context

class StorySectionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, MemberUpdateMixin, UpdateView):

    permission_required = 'documentation.change_storysection'
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

class StorySectionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, MemberDeleteMixin, DeleteView):

    permission_required = 'documentation.delete_storysection'
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
