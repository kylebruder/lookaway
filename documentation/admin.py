from django.contrib import admin
from .models import Document, DocumentSection, SupportDocument, SupportDocSection
# Register your models here.

admin.site.register(Document)
admin.site.register(DocumentSection)
admin.site.register(SupportDocument)
admin.site.register(SupportDocSection)

