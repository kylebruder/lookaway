from django.contrib import admin
from .models import MusicAppProfile, MusicPageSection, Album, Track

# Register your models here.

admin.site.register(MusicAppProfile)
admin.site.register(MusicPageSection)
admin.site.register(Track)
admin.site.register(Album)
