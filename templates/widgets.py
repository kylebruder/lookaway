from django.db import models
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput, Textarea

class ImagePreviewWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = '''<input type="file" name="image_file" \
        onchange="loadFile(event)"><br><br>\
        <img class="form-preview-image" id="output"/>'''
        return mark_safe(template)

class SoundPreviewWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = '''<input type="file" name="sound_file" \
        class="file_multi_media"><br><br>\
        <audio controls="controls">\
          <source src="" type="audio/midi" id="midi">\
          <source src="" type="audio/mpeg" id="mpeg">\
          <source src="" type="audio/ogg" id="ogg">\
          <source src="" type="audio/x-m4a" id="x-m4a">\
          <source src="" type="audio/x-realaudio" id="x-realaudio">\
        </audio>'''
        return mark_safe(template)

class VideoPreviewWidget(ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        template = '''<input type="file" name="video_file"\ 
        class="file_multi_media"><br><br>\
        <video class="video-player-sm" controls="controls">\
          <source src="" type="video/3gpp" id="3gpp">\
          <source src="" type="video/ts" id="ts">\
          <source src="" type="video/mp4" id="mp4">\
          <source src="" type="video/mpeg" id="mpeg">\
          <source src="" type="video/quicktime" id="quicktime">\
          <source src="" type="video/webm" id="webm">\
          <source src="" type="video/x-flv" id="x-flv">\
          <source src="" type="video/x-m4v" id="x-m4v">\
          <source src="" type="video/x-mng" id="x-mng">\
          <source src="" type="video/x-ms-asf" id="x-ms-asf">\
          <source src="" type="video/x-ms-wmv" id="x-ms-wmv">\
          <source src="" type="x-msvideo" id="x-msvideo">\
            Your Browser does not support embedded videos.\
        </video>'''
        return mark_safe(template)

class CodeWidget(Textarea):

    def render(self, name, value, attrs=None, renderer=None):
        template = '''<textarea wrap="off" class="code-box" name="code">\
        </textarea>'''
        return mark_safe(template)

class FictionWidget(CheckboxInput):

    def render(self, name, value, attrs=None, renderer=None):
        if value == None:
          checked = "checked"
        else:
          checked = ''

        template = '''<div class="custom-control custom-switch" style="padding-left: 0px;">\
          <span class="float-start" style="padding-right: 50px;">Non-Fiction</span>
          <input type="checkbox" class="custom-control-input" id="customSwitch1" name="{name}" {checked}>\
          <label class="custom-control-label" for="customSwitch1">\
          Fiction
          </label>
        </div>'''.format(name=name, checked=checked)
        return mark_safe(template)
