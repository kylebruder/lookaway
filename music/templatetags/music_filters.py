from django.template.defaulttags import register

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

