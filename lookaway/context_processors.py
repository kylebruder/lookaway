from django.template.defaulttags import register
from lookaway.settings import INSTALLED_APPS as APPS
from home.models import HomeAppProfile
'''
Custom context processors for site wide template context :)

* Fallback SEO title and description in case a view does not provide
* Customize the nav bar
* Add legal notices and contact email to every page
* Set the agreement text for the member registration page
'''

# Use the main AppProfile from the home app
profile, created = HomeAppProfile.objects.get_or_create(pk=1)

# SEO stuff
## In case we don't get a title sent to a template
def lookaway_seo(request):
    return {
        "lookaway_title": profile.title,
        "lookaway_meta_desc": profile.meta_description,
    }


# Navbar stuff
## Only show the app if it is installed and we want to show it. 
## The core apps, home, objects, members, posts, must be installed.
def nav_apps(request):
    if profile.nav_show_posts:
        show_posts = True
    else:
        show_posts = False
    if profile.nav_show_members:
        show_members = True
    else:
        show_members = False
    if 'documentation' in APPS and profile.nav_show_documentation:
        show_documentation = True
    else:
        show_documentation = False
    if 'art' in APPS and profile.nav_show_art:
        show_art = True
    else:
        show_art = False
    if 'music' in APPS and profile.nav_show_music:
        show_music = True
    else:
        show_music = False
    if profile.nav_show_objects:
        show_objects = True
    else:
        show_objects = False
    return {
        "nav_show_posts": show_posts,
        "nav_show_members": show_members,
        "nav_show_documentation": show_documentation,
        "nav_show_art": show_art,
        "nav_show_music": show_music,
        "nav_show_objects": show_objects,
    }

## Each app has a name and, optionally, an image.
## If the app has an image, it will be used instead of the name.
## Posts
def nav_buttons(request):
    buttons = {
        "nav_posts_name": profile.nav_posts_name,
        "nav_documentation_name": profile.nav_documentation_name,
        "nav_art_name": profile.nav_art_name,
        "nav_music_name": profile.nav_music_name,
        "nav_members_name": profile.nav_members_name,
        "nav_objects_name": profile.nav_objects_name,
    }
    if profile.nav_posts_image:
        buttons['nav_posts_image'] = profile.nav_posts_image.image_file.url
    if profile.nav_documentation_image:
        buttons['nav_documentation_image'] = profile.nav_documentation_image.image_file.url
    if profile.nav_art_image:
        buttons['nav_art_image'] = profile.nav_art_image.image_file.url
    if profile.nav_music_image:
        buttons['nav_music_image'] = profile.nav_music_image.image_file.url
    if profile.nav_members_image:
        buttons['nav_members_image'] = profile.nav_members_image.image_file.url
    if profile.nav_objects_image:
        buttons['nav_objects_image'] = profile.nav_objects_image.image_file.url
    return buttons

# Buttons

# Thanks culebrón! (So obvious now, *facepalm*)
# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
def lookup(dictionary, key):
    print(dictionary)
    return dictionary.get(key)
register.filter('lookup', lookup)

# Footer
def lookaway_footer(request):
    return {
        "lookaway_notice": profile.legal_notice,
        "lookaway_email": profile.admin_email,
    }

# CSS
## Use a different css file. This is optional. The base template uses
## '/static/style.css' if no path is specified. There is no built in validation
## for provided paths. Most browsers will fail silently if the given path is
## unavailable resulting in no styling.
def lookaway_css_path(request):
    return {
        "lookaway_css_path": profile.css_path
    }

## Objects

@register.filter
def get_domain(value):
    from urllib.parse import urlparse
    o = urlparse(value)
    return o.hostname

@register.filter
def highlight_sytax(code, path):
    from pygments import highlight
    from pygments.lexers import guess_lexer, get_lexer_for_filename
    from pygments.formatters import HtmlFormatter
    if path:
        lexer = get_lexer_for_filename(path)
    else:
        lexer = guess_lexer(code)
    formatter = HtmlFormatter(linenos=True, cssclass="source")
    return highlight(code, lexer, formatter)


## Music

@register.filter
def is_original_release(self):
    if not self.year:
        return True
    elif self.publication_date:
        if int(self.year) == int(self.publication_date.strftime("%Y")):
            return True
        else:
            return False
    else:
        return False
