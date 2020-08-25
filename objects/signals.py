import re
import logging
from bs4 import BeautifulSoup
from urllib import request as rq
from urllib.parse import urlparse
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from pathlib import Path
from PIL import Image as img
from PIL import ImageOps
from lookaway.settings import BASE_DIR
from .models import Image, Link
from .utils import FileSystemOps

logger = logging.getLogger(__name__)
# Images
@receiver(post_save, sender=Image)
def handle_image_upload(sender, instance, created, *args, **kwargs):
    '''
    Resizes the image for web format
    Add a thumbnail image to the Image model after it is saved to DB
    '''
    if created:
        image = img.open(instance.image_file.path)
        # Resize the original if it is bigger than 2500 by 2500
        # Transpose Exif tags if the image has them
        try:
            image = ImageOps.exif_transpose(image)
            image.save(q)
        except:
            print("no EXIF tags found")
        if image.width > 2500 or image.height > 2500:
            max_size = (2500, 2500)
            image.thumbnail(max_size)
            image.save(instance.image_file.path)
        # Create a thumbnail based on the uploaded image
        max_size = (250, 250)
        image.thumbnail(max_size)
        owner = instance.owner.id
        thumb_dir = instance.creation_date.strftime(
            'member_{0}/thumbnails/%Y/%m/%d/'.format(owner)
        )
        file_name = instance.image_file.name.split('/')[-1].split('.')[0]
        extension = instance.image_file.name.split('/')[-1].split('.')[-1]
        thumb_file_name = '{}{}{}'.format(file_name, '-thumbnail.', extension)
        p = Path('media')
        q = BASE_DIR / p / thumb_dir
        Path.mkdir(q, parents=True, exist_ok=True)
        image.save(q / thumb_file_name)
        image.close()
        p = Path(thumb_dir)
        q = p / thumb_file_name
        instance.thumbnail_file = str(q)
        instance.save()
    else:
       pass 

@receiver(post_delete, sender=Image)
def remove_image_files(sender, instance, *args, **kwargs):
    '''
    Remove image files related to the deleted Image instance from the filesystem
    '''
    fsop = FileSystemOps()
    if instance.image_file:
        fsop._delete_file(instance.image_file.path)
    if instance.thumbnail_file:
        fsop._delete_file(instance.thumbnail_file.path)

# Links


@receiver(post_save, sender=Link)
def scrape_link_fields(sender, instance, created, *args, **kwargs):
    '''
    Scrape title, description and favicon URI from URL
    '''
    if created and instance.url:
        # Check the instance URL for a good response
        try:
            response = rq.urlopen(instance.url)
            if response.getcode() in (200, 300, 301, 302):
                soup = BeautifulSoup(response, 'html.parser')
                # Look for a title
                try:
                    instance.title = soup.find('title').string
                except:
                    pass
                # Look for a description
                try:
                    instance.text = soup.find('meta', {'name': 'description'}).get('content')
                except:
                    instance.text = soup.p
                # Look for the favicon
                try:
                    href = soup.find('link',  attrs={'rel':'shortcut icon'}).get('href')
                except:
                    href = ''
                if href != '':
                    o = urlparse(href)
                    # Ensure HTTPS in URI and FQDN
                    if o[0] == 'https' and o[1]:
                        instance.favicon_href = href
                        print(instance.favicon_href)
                    # If no FQDN append the relative path to the FQDN
                    else:
                        url = urlparse(instance.url)
                        # Ensure HTTPS in URI
                        if url[0] == 'https':
                            href = url[0] + '://' + url[1] + href
                            instance.favicon_href = href
                            print(instance.favicon_href)
                post_save.disconnect(scrape_link_fields, sender=Link)
                try:
                    instance.save()
                except:
                    pass
                post_save.connect(scrape_link_fields, sender=Link)
        except:
            pass
