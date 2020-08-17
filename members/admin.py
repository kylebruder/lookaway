from django.contrib import admin
from .models import Member, Marshmallow, Profile, InviteLink
# Register your models here.

admin.site.register(Member)
admin.site.register(Marshmallow)
admin.site.register(Profile)
admin.site.register(InviteLink)
