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
from lookaway.settings import BASE_DIR, MEDIA_ROOT
from .models import ObjectsAppProfile, Image, Sound, Video, Link
from .utils import FileSystemOps

logger = logging.getLogger(__name__)

# Transcoder settings
    

# Upload handlers

@receiver(post_save, sender=Image)
def handle_image_upload(sender, instance, created, *args, **kwargs):
    profile, new = ObjectsAppProfile.objects.get_or_create(pk=1)
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
        # Image settings
        w = profile.image_max_width
        h = profile.image_max_height
        if profile.image_format == "JPG":
            img_format = "jpeg"
        else:
            img_format = "webp"
        # Resize the original if the height or width are 
        # larger than the height and width specidied in settings
        if image.width > w or image.height > h:
            max_size = (w, h)
            image.thumbnail(max_size)
            info = image.info
            try:
                image.save(instance.image_file.path, img_format, **info)
            except:
                img_format = 'webp'
                image.save(instance.image_file.path, img_format, **info)

        # Give the image a random name and webp extenstion
        instance.title = original_name.split('.')[:-1][0][0:63]
        img_path = Path(instance.image_file.path)
        seed = str(img_path) + str(timezone.now())
        safe_file_name = md5(seed.encode()).hexdigest() + '.' + img_format
        new_path = img_path.rename(img_path.parent / safe_file_name)
        instance.image_file = str(new_path.relative_to(MEDIA_ROOT))
        instance.save()

        # Create a thumbnail based on the uploaded image
        h = profile.thumbnail_max_height
        w = profile.thumbnail_max_width
        max_size = (h, w)
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
        try:
            image.save(q / thumb_file_name, img_format)
        except:
            img_format = 'webp'
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
    profile, new = ObjectsAppProfile.objects.get_or_create(pk=1)
    if created:
        snd_file = instance.sound_file.path
        # Thanks derekkwok!
        # https://gist.github.com/derekkwok/4077509
        # Sound settings
        ffmpeg_cmd = profile.ffmpeg_path
        bitrate = str(profile.sound_bitrate)
        crf = str(profile.sound_crf)
        qmin = str(profile.sound_qmin)
        qmax = str(profile.sound_qmax)
        if profile.sound_format == "MP3":
            snd_ext = ".mp3"
        else:
            snd_ext = ".ogg"

        def encode(snd_file):
            path = ''.join(snd_file.split('.')[:-1])
            # Add a "1" to file name if the file is already using the extension configured.
            # This avoids erroring when trying to convert a file to a new file of  the smae filename.
            if snd_ext in snd_file:
                output = '{}1{}'.format(path, snd_ext)
            else:
                output = '{}{}'.format(path, snd_ext)
            # Thanks Vestride
            # https://gist.github.com/Vestride/278e13915894821e1d6f
            command = [
                ffmpeg_cmd,
                '-y',
                '-i', snd_file,
                '-qmin', qmin,
                '-qmax', qmax,
                '-b:v', bitrate,
                '-crf', crf,
                '-deadline', 'realtime',
                output
            ]
            subprocess.call(command)
            #Delete the original upload
            fsop = FileSystemOps()
            fsop._delete_file(instance.sound_file.path)
            return output

        try:
            # Transcode the uploaded file
            snd_path = Path(encode(snd_file))
            # Give the image a random name and webp extenstion
            original_name = Path(snd_file).name
            instance.title = original_name.split('.')[:-1][0][:63]
            seed = str(snd_path) + str(timezone.now())
            safe_file_name = md5(seed.encode()).hexdigest() + snd_ext
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
    profile, new = ObjectsAppProfile.objects.get_or_create(pk=1)
    if created:
        vid_file = instance.video_file.path
        # Thanks derekkwok!
        # https://gist.github.com/derekkwok/4077509
        # Video settings
        ffmpeg_cmd = profile.ffmpeg_path
        bitrate = str(profile.video_bitrate)
        crf = str(profile.video_crf)
        qmin = str(profile.video_qmin)
        qmax = str(profile.video_qmax)
        if profile.video_format == "MP4":
            vid_ext = ".mp4"
        else:
            vid_ext = ".webm"
        
        def encode(vid_file):
            path = ''.join(vid_file.split('.')[:-1])
            # Add a "1" to file name if the file is already using the extension configured.
            # This avoids erroring when trying to convert a file to a new file of  the smae filename.
            if vid_ext in vid_file:
                output = '{}1{}'.format(path, vid_ext)
            else:
                output = '{}{}'.format(path, vid_ext)
            output = '{}.{}'.format(path, vid_ext)
            # Thanks Vestride
            # https://gist.github.com/Vestride/278e13915894821e1d6f
            command = [
                ffmpeg_cmd,
                '-y',
                '-i', vid_file,
                '-qmin', qmin,
                '-qmax', qmax,
                '-b:v', bitrate,
                '-crf', crf,
                '-deadline', 'realtime',
                output
            ]
            subprocess.call(command)
            #Delete the original upload
            fsop = FileSystemOps()
            fsop._delete_file(instance.video_file.path)
            return output
                
        try:
            # Transcode the uploaded file
            vid_path = Path(encode(vid_file))
            # Give the image a random name and webp extenstion
            original_name = Path(vid_file).name
            instance.title = original_name.split('.')[:-1][0][:63]
            seed = str(vid_path) + str(timezone.now())
            safe_file_name = md5(seed.encode()).hexdigest() + vid_ext
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
