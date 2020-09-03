from django.shortcuts import render
from django.views.generic.base import TemplateView
from posts.models import Post
# Create your views here.

class IndexView(TemplateView):

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            is_public=True,
            members_only=False,
            re=None,
        )[:10]
        return context
