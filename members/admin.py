from django.contrib import admin
from .models import Member, MembersAppProfile, MembersPageSection, Marshmallow, Profile, MemberProfileSection, InviteLink
# Register your models here.

admin.site.register(Member)
admin.site.register(MembersAppProfile)
admin.site.register(MembersPageSection)
admin.site.register(Marshmallow)
admin.site.register(Profile)
admin.site.register(MemberProfileSection)
admin.site.register(InviteLink)
