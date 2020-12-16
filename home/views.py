from django.shortcuts import render
from django.views.generic.base import TemplateView
from art.models import Gallery, Visual
from music.models import Album, Track
from objects.models import Tag
from documentation.models import Article, Story, SupportDocument
from posts.models import Post

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
        context['posts'] = Post.objects.filter(
            is_public=True,
            members_only=False,
            re=None,
        ).order_by(
            '-publication_date',
        )[:20]
        context['articles'] = Article.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:20]
        context['stories'] = Story.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:20]
        context['documents'] = SupportDocument.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:20]
        context['visuals'] = Visual.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:16]
        context['galleries'] = Gallery.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:5]
        context['tracks'] = Track.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:4]
        context['albums'] = Album.objects.filter(
            is_public=True,
        ).order_by(
            '-publication_date',
        )[:5]
        return context
