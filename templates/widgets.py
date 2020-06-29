from django.db import models
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput

class ImagePreviewWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = '<input type=\'file\' name=\'image_file\' onchange="loadFile(event)"><br><br><img class="updates-form-image" id="output"/>'
        return mark_safe(template)
