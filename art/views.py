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
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from members.models import Member
from members.mixins import MemberOwnershipView, MemberDeleteView
from .forms import GalleryForm, VisualForm
from .models import Gallery, Visual
# Create your views here.

# Gallery Views

class ArtPageView(TemplateView):

    template_name = 'art/art_page.html'

    def get_context_data(self, **kwargs):
        # Number of items to show in each list
        n = 5
        context = super().get_context_data(**kwargs)
        # Galleries
        public_galleries = Gallery.objects.filter(is_public=True)
        if public_galleries.count() >= n:
            print("There are {} or more published Galleries".format(n))
            # Get the date of the 5th newest Gallery
            # if there are 5 or more Galleries.
            last_new_gallery_date = public_galleries.order_by(
                '-publication_date',
            )[n-1].publication_date
            # Get the 5 newest Galleries.
            context['new_galleries'] = public_galleries.order_by(
                '-publication_date',
            )[:n]
            # Exclude any Gallery that appears in the new galleries list
            # from the top Gallery list.
            context['top_galleries'] = public_galleries.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_gallery_date,
            )[:n]
            print("New Galleries: {}".format(context['new_galleries']))
            print("Top Galleries: {}".format(context['top_galleries']))
        # If there are less than 5 Galleries,
        # include all of them in the new Gallery list.
        else:
            print("There are less than 5 published Galleries")
            context['new_galleries'] = public_galleries.order_by(
                '-publication_date',
            )
            print(context['new_galleries'])

        # Visuals
        public_visuals = Visual.objects.filter(is_public=True)
        if public_visuals.count() >= n*6:
            print("There are {} or more published Visuals".format(n))
            # Get the date of the nth newest Visual
            # if there are n*6 or more Visuals
            last_new_visual_date = public_visuals.order_by(
                '-publication_date',
            )[n*6-1].publication_date
            context['new_visuals'] = public_visuals.order_by(
                '-publication_date',
            )[:n*6]
            print("New Visuals: ", context['new_visuals'])
            # Exclude any Gallery that appears in the new releases list
            # from the top Visual list
            context['top_visuals'] = public_visuals.order_by(
                '-weight',
            ).exclude(
                publication_date__gte=last_new_visual_date,
            )[:n*6]
            print("Top Visuals: ", context['top_visuals'])
        else:
            print("There are less than {} published Visuals".format(n))
            context['new_visuals'] = public_visuals.order_by(
                '-publication_date',
            )[:n*6]
            print(context['new_visuals'])
        return context

class GalleryCreateView(LoginRequiredMixin, CreateView):

    model = Gallery
    form_class = GalleryForm

    def get_form_kwargs(self):
        kwargs = super(GalleryCreateView, self).get_form_kwargs()
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
                'art:gallery_detail',
                kwargs={'slug': self.object.slug},
            )

class GalleryListView(ListView):

    model = Gallery
    paginate_by = 6
    context_object_name = 'galleries'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Gallery.objects.filter(
                is_public=True,
            ).order_by(
                '-creation_date',
            )
        else:
            return Gallery.objects.filter(
                is_public=True,
            ).order_by(
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class TopGalleryListView(ListView):

    model = Gallery
    paginate_by = 6
    context_object_name = 'galleries'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Gallery.objects.filter(
                is_public=True,
            ).order_by(
                '-weight',
                '-creation_date',
            )
        else:
            return Gallery.objects.filter(
                is_public=True,
            ).order_by(
                '-weight',
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context

class GalleryDetailView(DetailView):

    model = Gallery
    context_object_name = 'gallery'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class MemberGalleryView(ListView):

    model = Gallery
    paginate_by = 6
    context_object_name = 'galleries'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Gallery.objects.filter(
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

class GalleryUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Gallery
    form_class = GalleryForm

    def get_form_kwargs(self):
        kwargs = super(GalleryUpdateView, self).get_form_kwargs()
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
                'art:gallery_detail',
                kwargs={'slug': self.object.slug},
            )

class GalleryDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Gallery

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_gallery_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Gallery, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Gallery)
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
    return HttpResponseRedirect(reverse('art:top_galleries'))

def publish_gallery_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Gallery, pk=pk)
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
                    'art:gallery_detail',
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
                'art:gallery_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

# Visual Views

class VisualCreateView(LoginRequiredMixin, CreateView):

    model = Visual
    form_class = VisualForm

    def get_form_kwargs(self):
        kwargs = super(VisualCreateView, self).get_form_kwargs()
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
            return reverse_lazy(
                'art:visual_detail',
                kwargs={'slug': self.object.slug},
            )

class VisualListView(ListView):

    model = Visual
    paginate_by = 36
    context_object_name = 'visuals'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Visual.objects.filter(
                is_public=True,
            ).order_by(
                '-creation_date',
            )
        else:
            return Visual.objects.filter(
                is_public=True,
            ).order_by(
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = True
        return context

class TopVisualListView(ListView):

    model = Visual
    paginate_by = 36
    context_object_name = 'visuals'

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return Visual.objects.filter(
                is_public=True,
            ).order_by(
                '-weight',
                '-creation_date',
            )
        else:
            return Visual.objects.filter(
                is_public=True,
            ).order_by(
                '-weight',
                '-creation_date',
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top'] = True
        return context

class VisualDetailView(DetailView):

    model = Visual
    context_object_name = 'visual'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            member = Member.objects.get(pk=self.request.user.pk)
            if member.check_can_allocate() and not member.check_is_new():
                context['can_add_marshmallow'] = True
            else:
                context['can_add_marshmallow'] = False
        return context

class MemberVisualView(ListView):

    model = Visual
    paginate_by = 6
    context_object_name = 'visuals'

    def get_queryset(self, *args, **kwargs):
        member = Member.objects.get(username=self.kwargs['member'])
        return Visual.objects.filter(
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

class VisualUpdateView(LoginRequiredMixin, MemberOwnershipView, UpdateView):

    model = Visual
    form_class = VisualForm

    def get_form_kwargs(self):
        kwargs = super(VisualUpdateView, self).get_form_kwargs()
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
                'art:visual_detail',
                kwargs={'slug': self.object.slug},
            )

class VisualDeleteView(LoginRequiredMixin, MemberDeleteView, DeleteView):

    model = Visual

    def get_success_url(self):
        return reverse('members:studio')

def add_marshmallow_to_visual_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Visual, pk=pk)
    if instance.is_public:
        successful, instance, weight = member.allocate_marshmallow(instance, model=Visual)
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
    return HttpResponseRedirect(reverse('art:top_visuals'))

def publish_visual_view(request, pk):
    member = Member.objects.get(pk=request.user.pk)
    instance = get_object_or_404(Visual, pk=pk)
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
                    'art:visual_detail',
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
                'art:visual_detail',
                kwargs={'pk': instance.pk}
            )
        )
    else:
        return HttpResponseRedirect(reverse('member:studio'))

