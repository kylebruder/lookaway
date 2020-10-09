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
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberOwnershipView, MemberDeleteView
from .forms import DocumentForm, DocumentSectionForm, SupportDocumentForm, SupportDocSectionForm
from .models import Document, DocumentSection, SupportDocument, SupportDocSection

# Create your views here.

# Support Document Views

class DocumentCreateView(LoginRequiredMixin, CreateView):

    model = Document
    form_class = DocumentForm

    def get_form_kwargs(self):
        kwargs = super(DocumentCreateView, self).get_form_kwargs()
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
                'documentation:document_detail',
                kwargs={'slug': self.object.slug},
            )

class DocumentListView(ListView):

    model = Document
    paginate_by = 20
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        return Document.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-creation_date',
        )
    
class MemberDocumentView(LoginRequiredMixin, ListView):

    model = Document
    paginate_by = 20
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Document.objects.filter(
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

class DocumentDetailView(DetailView):

    model = Document
    context_object_name = 'document'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        context['sections'] = DocumentSection.objects.filter(
            document=self.get_object(),
        ).order_by('order')
        return context

class DocumentUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Document
    form_class = DocumentForm

    def get_form_kwargs(self):
        kwargs = super(DocumentUpdateView, self).get_form_kwargs()
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
                'documentation:document_detail',
                kwargs={'slug': self.object.slug},
            )

class DocumentDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Document

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_document_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Document, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Document)
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
    return HttpResponseRedirect(reverse('documentation:public_documents'))

def publish_document_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Document, pk=pk)
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
                    'documentation:document_detail',
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
                'documentation:document_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# DocumentSection Views

class DocumentSectionCreateView(LoginRequiredMixin, CreateView):

    model = DocumentSection
    form_class = DocumentSectionForm

    def get_form_kwargs(self):
        kwargs = super(DocumentSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
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
                'documentation:document_section_detail',
                kwargs={'pk': self.object.pk},
            )

class MemberDocumentSectionView(LoginRequiredMixin, ListView):

    model = DocumentSection
    paginate_by = 20
    context_object_name = 'sections'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return DocumentSection.objects.filter(owner=member)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = Member.objects.get(username=self.kwargs['member'])
        context['user_only'] = True
        context['member'] = member
        return context

class DocumentSectionDetailView(LoginRequiredMixin, DetailView):

    model = DocumentSection
    context_object_name = 'section'

class DocumentSectionUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = DocumentSection
    form_class = DocumentSectionForm

    def get_form_kwargs(self):
        kwargs = super(DocumentSectionUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Update last modified date for the DocumentSection
        form.instance.last_modified = timezone.now()
        # Update last modified date for the parent Document too
        print(Document.objects.get(
            pk=form.instance.document.pk
        ) )
        s = Document.objects.get(
            pk=form.instance.document.pk
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
                'documentation:document_section_detail',
                kwargs={'pk': self.object.pk},
            )

class DocumentSectionDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = DocumentSection

    def get_success_url(self):
        return reverse('members:studio')

# Support Document Views

class SupportDocumentCreateView(LoginRequiredMixin, CreateView):

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
    paginate_by = 20
    context_object_name = 'documents'

    def get_queryset(self, *args, **kwargs):
        return SupportDocument.objects.filter(
            is_public=True,
        ).order_by(
            '-weight',
            '-creation_date',
        )
    
class MemberSupportDocumentView(LoginRequiredMixin, ListView):

    model = SupportDocument
    paginate_by = 20
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

class SupportDocumentUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

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

class SupportDocumentDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = SupportDocument

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_support_document_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(SupportDocument, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=SupportDocument)
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

class SupportDocSectionCreateView(LoginRequiredMixin, CreateView):

    model = SupportDocSection
    form_class = SupportDocSectionForm

    def get_form_kwargs(self):
        kwargs = super(SupportDocSectionCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
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
    paginate_by = 20
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

class SupportDocSectionUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

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

class SupportDocSectionDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = SupportDocSection

    def get_success_url(self):
        return reverse('members:studio')
