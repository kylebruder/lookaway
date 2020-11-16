from django.contrib import admin
from .models import Article, ArticleSection, Story, StorySection, SupportDocument, SupportDocSection
# Register your models here.

admin.site.register(Article)
admin.site.register(ArticleSection)
admin.site.register(Story)
admin.site.register(StorySection)
admin.site.register(SupportDocument)
admin.site.register(SupportDocSection)

