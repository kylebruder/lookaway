from django.contrib import admin
from .models import PostsAppProfile, PostsPageSection, Post, ResponsePost

# Register your models here.

admin.site.register(PostsAppProfile)
admin.site.register(PostsPageSection)
admin.site.register(Post)
admin.site.register(ResponsePost)
