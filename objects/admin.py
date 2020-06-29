from django.contrib import admin
from .models import Tag, Image, Sound, Code, Link

# Register your models here.

admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Sound)
admin.site.register(Code)
admin.site.register(Link)
