from django.db import models
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput, Textarea

class ImagePreviewWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = '<input type="file" name="image_file" onchange="loadFile(event)"><br><br><img class="form-preview-image" id="output"/>'
        return mark_safe(template)

class SoundPreviewWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = '<input type="file" name="sound_file" onchange="loadFile(event)"><br><br><audio controls="controls" src="" type="audio/mpeg" id="output"></audio>'
        return mark_safe(template)

class VideoPreviewWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = '<input type="file" name="video_file" class="file_multi_video"><br><br><video class="video-player-sm" controls><source src="" type="video/mp4" id="video_here">Your Browser does not support embedded videos.</video>'
        return mark_safe(template)

class CodeWidget(Textarea):

    def render(self, name, value, attrs=None, renderer=None):
        template = '<textarea wrap="off" class="code-box" name="code"></textarea>'
        return mark_safe(template)
