import os
from io import BytesIO
from pathlib import Path
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from members.models import Member
from .models import Image, Sound

class FileSystemOps:

    def __init__(self, *args, **kwargs):
        pass

    def _delete_file(self, path):
        '''
        Delete a file from the filesystem
        '''
        f = Path(path)
        if f.is_file():
            f.unlink()
            return 0
        else:
            return 1

    def _make_dir(self, path):
        '''
        Checks to see if a path exists as a directory.
        If the path exists but is a file, return 1.
        If the path does not exist, create the directory, return 0.
        If the path exists and is a directory, return -1.
        '''
        f = Path(path)
        if f.is_file():
            return 1
        elif f.is_dir():
            return 0
        else:
            f.mkdir
            return -1

class Text:
    '''
    Utilities for changing text
    '''
    def __init__(self, *args, **kwargs):
        pass

    def slugify_unique(model, title):
        '''
        Given a DB model and a title, return a unique slug that is unique \
        to all other slug fields of the given DB model.
        
        Arguments
        model - Must be a Django database model that has \
                   a slug field called "slug".
        title - The string used to create the slug.

        Returns - A slug that is unique across all instances of the model.
        '''
        from django.utils.text import slugify
        slug = slugify(title)
        existing_slugs = []
        try:
            [existing_slugs.append(str(i.slug)) for i in model.objects.all()]
        except:
            print("There was no slug field found for {}".format(model))
            return slug
        if slug in existing_slugs:
            date_slug = slug + "-" + timezone.now().strftime("%Y%m%d")
            if date_slug in existing_slugs:
                long_slug = date_slug + timezone.now().strftime("%m%s")
                return long_slug
            else:
                return date_slug
        else:
            return slug
        
class TestData:

    def __init__(self, *args, **kwargs):
        pass

    # Text
    big_text = """Lorem ipsum dolor sit amet, consectetur adipiscing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
mollit anim id est laborum."""
    small_text = "Duis aute irure dolor"
    email = "fred@slate.rock"
    first_name = "Fred"
    last_name = "Flinstone"
    password = "testpassword"
    tiny_text = "1.4a"
    url = "https://www.google.com"
    username = "fflinstone"
    
    # File paths
    image_path = os.path.join(settings.BASE_DIR, 'media/test.png')
    sound_path = os.path.join(settings.BASE_DIR, 'media/test.wav')

    def create_test_member(self):
        '''
        Create a test member.
        Returns the Member and proxied User 
        '''
        member = Member.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        user = User.objects.get(pk=member.pk)
        return member, user

    def code_data(self):
        '''
        Returns test data for Code views.
        '''
        data = {
            'title': self.small_text,
            'code': self.big_text,
            'language': self.small_text,
            'language_version': self.tiny_text,
            'file_path': self.small_text,
            'source': self.small_text,
        }
        return data
        

    def link_data(self):
        '''
        Returns test data for Link views.
        '''
        data = {
            'title': self.small_text,
            'text': self.big_text,
            'url': self.url
        }
        return data

    def small_image(self, member):
        '''
        Given a Member instance, creates an image in the database.
        Returns test data for Image views and a raw image file.
        '''
        # Create test image in media dir
        from PIL import Image as image
        test_image = image.new('RGB', (500, 500))
        test_image.save(self.image_path, "PNG")
        with open(self.image_path, 'rb') as f:
            img = BytesIO(b'f')
            img.name = "test.png"
            data = {
                'title': self.small_text,
                'image_file': self.image_path.split('/')[-1],
                'text': self.big_text,
                'credit': self.small_text,
            }
            image = Image.objects.create(owner=member, **data)
            image.save()
            return data, img

    def small_sound(self, member):
        '''
        Given a Member instance, creates a sound in the database.
        Returns test data for sound views and a raw sound file
        '''
        # Create test sound in media dir
        # https://medium.com/@jxxcarlson/creating-audio-files-with-python-55cba61bfe73
        import numpy as np
        import wavio
        # Parameters
        rate = 44100    # samples per second
        T = 150         # sample duration (seconds)
        f = 440.0       # sound frequency (Hz)
        # Compute waveform samples
        t = np.linspace(0, T, T*rate, endpoint=False)
        x = np.sin(2*np.pi * f * t)
        # Write the samples to a file
        wavio.write(self.sound_path, x, rate, sampwidth=3)
        with open(self.sound_path, 'rb') as f:
            smp = BytesIO(b'f')
            smp.name = "test.wav"
            data = {
                'title': self.small_text,
                'sound_file': self.sound_path.split('/')[-1],
                'text': self.big_text,
                'credit': self.small_text,
            }
            sound = Sound.objects.create(owner=member, **data)
            sound.save()
            return data, smp
