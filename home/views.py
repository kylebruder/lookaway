from django.shortcuts import render
from django.views.generic.base import TemplateView
from art.models import Gallery, Visual
from music.models import Album, Track
from objects.models import Tag
from documentation.models import Article, Story, SupportDocument
from posts.models import Post
from .models import HomeAppProfile, HomePageSection

# Create your views here.

class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Create a public object tags context
        public_tags = Tag.objects.none()
        tag_models = {Post, Gallery, Visual, Album, Track, Article, SupportDocument}
        for model in tag_models:
            public_tags = public_tags | Tag.get_tags_from_public(model)
        context['tags'] = public_tags.order_by('-weight')[:50]
        # Sections
        sections = HomePageSection.objects.filter(
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
        context['posts'] = Post.objects.filter(
            is_public=True,
            members_only=False,
            re=None,
        ).order_by(
            '-publication_date',
        )[:50]
        context['articles'] = Article.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:10]
        context['stories'] = Story.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:10]
        context['documents'] = SupportDocument.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:10]
        context['visuals'] = Visual.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:9]
        context['galleries'] = Gallery.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:3]
        context['tracks'] = Track.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:3]
        context['albums'] = Album.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:3]
        return context
