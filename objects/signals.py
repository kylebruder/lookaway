import logging
import re
import shutil
import subprocess
from bs4 import BeautifulSoup
from urllib import request as rq
from urllib.parse import urlparse
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from hashlib import md5
from pathlib import Path
from PIL import Image as img
from PIL import ImageOps
from lookaway.settings import BASE_DIR, MEDIA_ROOT, MEDIA_SETTINGS
from .models import Image, Sound, Video, Link
from .utils import FileSystemOps

logger = logging.getLogger(__name__)

# Upload handlers

@receiver(post_save, sender=Image)
def handle_image_upload(sender, instance, created, *args, **kwargs):
    '''
    Resize images with a width or height > values
    from the main Lookaway settings file.
    Converts valid image files to webp.
    Adds a thumbnail image to the Image model.
    '''
    if created:
        # Start with the raw uploaded image
        image = img.open(instance.image_file.path)
        original_name = Path(image.filename).name

        # Attempt to transpose Exif tags if the image has them
        try:
            image = ImageOps.exif_transpose(image)
            image.save(instance.image_file.path)
        except:
            logger.error(
                'exif tag tranposition failed for image {} with pk {}'.format(
                    instance,
                    instance.pk,
                )
            )
        # Resize the original if the height or width are 
        # larger than the height and width specidied in settings
        h = MEDIA_SETTINGS['image']['max_height']
        w = MEDIA_SETTINGS['image']['max_width']
        img_format = "webp"
        if image.width > w or image.height > h:
            max_size = (w, h)
            image.thumbnail(max_size)
            info = image.info
            image.save(instance.image_file.path, img_format, **info)

        # Give the image a random name and webp extenstion
        instance.title = original_name.split('.')[:-1][0]
        img_path = Path(instance.image_file.path)
        seed = str(img_path) + str(timezone.now())
        safe_file_name = md5(seed.encode()).hexdigest() + '.' + img_format
        new_path = img_path.rename(img_path.parent / safe_file_name)
        instance.image_file = str(new_path.relative_to(MEDIA_ROOT))
        instance.save()

        # Create a thumbnail based on the uploaded image
        h = MEDIA_SETTINGS['image']['thumbnail']['max_height']
        w = MEDIA_SETTINGS['image']['thumbnail']['max_width']
        img_format = "webp"
        max_size = (250, 250)
        image.thumbnail(max_size)
        owner = instance.owner.id
        thumb_dir = instance.creation_date.strftime(
            'member_{0}/thumbnails/%Y/%m/%d/'.format(owner)
        )
        file_name = instance.image_file.name.split('/')[-1].split('.')[0]
        thumb_file_name = '{}{}{}'.format(
            file_name,
            '-thumbnail.',
            img_format,
        )
        p = Path(MEDIA_ROOT)
        q = p / thumb_dir
        Path.mkdir(q, parents=True, exist_ok=True)
        image.save(q / thumb_file_name, img_format)
        image.close()
        p = Path(thumb_dir)
        q = p / thumb_file_name
        instance.thumbnail_file = str(q)
        instance.save()
    else:
       pass 

@receiver(post_save, sender=Sound)
def handle_sound_upload(sender, instance, created, *args, **kwargs):
    '''
    Converts valid audio files into ogg.
    Sets the instance title to the filename minus the extension.
    Changes the filename on disk to a hard to guess name
    for added privacy.
    '''
    if created:
        snd_file = instance.sound_file.path
        # Thanks derekkwok!
        # https://gist.github.com/derekkwok/4077509
        ffmpeg_cmd = MEDIA_SETTINGS['ffmpeg_path']
        bitrate = MEDIA_SETTINGS['sound']['bitrate']
        crf = MEDIA_SETTINGS['sound']['crf']
        qmin = MEDIA_SETTINGS['sound']['qmin']
        qmax = MEDIA_SETTINGS['sound']['qmax']

        def encode(snd_file):
            path = ''.join(snd_file.split('.')[:-1])
            output = '{}.ogg'.format(path)
            # Thanks Vestride
            # https://gist.github.com/Vestride/278e13915894821e1d6f
            try:
                command = [
                    ffmpeg_cmd,
                    '-i', snd_file,
                    '-qmin', '0',
                    '-qmax', '50',
                    '-b:v', '1000K',
                    '-crf', crf,
                    '-deadline', 'realtime',
                    '-acodec', 'libvorbis',
                    output
                ]
                subprocess.call(command)
                return output
            except:
                logger.error(
                    'Transcoding failed for sound {} with pk {}'.format(
                        instance,
                        instance.pk,
                    )
                )
            finally:
                #Delete the original upload
                fsop = FileSystemOps()
                fsop._delete_file(instance.sound_file.path)

        try:
            # Transcode the uploaded file
            snd_path = Path(encode(snd_file))
            # Give the image a random name and webp extenstion
            original_name = Path(snd_file).name
            instance.title = original_name.split('.')[:-1][0][:63]
            seed = str(snd_path) + str(timezone.now())
            safe_file_name = md5(seed.encode()).hexdigest() + ".ogg"
            new_path = snd_path.rename(snd_path.parent / safe_file_name)
            instance.sound_file = str(new_path.relative_to(MEDIA_ROOT))
            instance.save()
        except:
            instance.title = "failed upload"
            instance.save()
            logger.error(
                'Transcoding failed for sound {} with pk {}'.format(
                    instance,
                    instance.pk,
                )
            )

@receiver(post_save, sender=Video)
def handle_video_upload(sender, instance, created, *args, **kwargs):
    '''
    Converts valid video files into webm.
    Sets the instance title to the filename minus the extension.
    Changes the filename on disk to a hard to guess name
    for added privacy.
    '''
    if created:
        vid_file = instance.video_file.path
        # Thanks derekkwok!
        # https://gist.github.com/derekkwok/4077509
        ffmpeg_cmd = MEDIA_SETTINGS['ffmpeg_path']
        bitrate = MEDIA_SETTINGS['video']['bitrate']
        crf = MEDIA_SETTINGS['video']['crf']
        qmin = MEDIA_SETTINGS['video']['qmin']
        qmax = MEDIA_SETTINGS['video']['qmax']
        
        def encode(vid_file):
            path = ''.join(vid_file.split('.')[:-1])
            output = '{}.webm'.format(path)
            # Thanks Vestride
            # https://gist.github.com/Vestride/278e13915894821e1d6f
            try:
                command = [
                    ffmpeg_cmd,
                    '-i', vid_file,
                    '-vcodec', 'libvpx', 
                    '-qmin', qmin,
                    '-qmax', qmax,
                    '-b:v', bitrate,
                    '-crf', crf,
                    '-deadline', 'realtime',
                    '-acodec', 'libvorbis',
                    output
                ]
                subprocess.call(command)
                return output
            except:
                logger.error(
                    'Transcoding failed for video {} with pk {}'.format(
                        instance,
                        instance.pk,
                    )
                )
                return 1
            finally:
                #Delete the original upload
                fsop = FileSystemOps()
                fsop._delete_file(instance.video_file.path)
                
        try:
            # Transcode the uploaded file
            vid_path = Path(encode(vid_file))
            # Give the image a random name and webp extenstion
            original_name = Path(vid_file).name
            instance.title = original_name.split('.')[:-1][0][:63]
            seed = str(vid_path) + str(timezone.now())
            safe_file_name = md5(seed.encode()).hexdigest() + ".webm"
            new_path = vid_path.rename(vid_path.parent / safe_file_name)
            instance.video_file = str(new_path.relative_to(MEDIA_ROOT))
            instance.save()
        except:
            instance.title = "failed upload"
            instance.save()
            logger.error(
                'Transcoding failed for video {} with pk {}'.format(
                    instance,
                    instance.pk,
                )
            )
    
# Cleanup
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

@receiver(post_delete, sender=Sound)
def remove_sound_file(sender, instance, *args, **kwargs):
    '''
    Remove sound file related to the deleted Sound instance from the filesystem
    '''
    fsop = FileSystemOps()
    if instance.sound_file:
        fsop._delete_file(instance.sound_file.path)

@receiver(post_delete, sender=Video)
def remove_video_file(sender, instance, *args, **kwargs):
    '''
    Remove video file related to the deleted Video instance from the filesystem
    '''
    fsop = FileSystemOps()
    if instance.video_file:
        fsop._delete_file(instance.video_file.path)

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
                    pass
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
                    # If no FQDN append the relative path to the FQDN
                    else:
                        url = urlparse(instance.url)
                        # Ensure HTTPS in URI
                        if url[0] == 'https':
                            href = url[0] + '://' + url[1] + href
                            instance.favicon_href = href
                post_save.disconnect(scrape_link_fields, sender=Link)
                try:
                    instance.save()
                except:
                    pass
        except:
            pass
