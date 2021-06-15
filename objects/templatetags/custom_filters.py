from django import template

register = template.Library()

## Objects

@register.filter
def get_domain(value):
    from urllib.parse import urlparse
    o = urlparse(value)
    return o.hostname

@register.filter(needs_autoescape=True)
def highlight_syntax(code, path, autoescape=True):
    from pygments import highlight
    from pygments.lexers import guess_lexer, get_lexer_for_filename
    from pygments.formatters import HtmlFormatter
    from django.utils.safestring import mark_safe
    if path:
        try:
            lexer = get_lexer_for_filename(path)
        except:
            lexer = guess_lexer(code)
    else:
        lexer = guess_lexer(code)
    formatter = HtmlFormatter(cssclass="highlight code-block", style="friendly")
    return mark_safe(highlight(code, lexer, formatter))
