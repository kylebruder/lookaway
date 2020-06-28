from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pathlib import Path
from PIL import Image as img
from PIL import ImageOps
from .models import Image

def _delete_file(path):
    '''
    Delete a file from the filesystem
    '''
    f = Path(path)
    if f.is_file():
        f.unlink()

@receiver(post_save, sender=Image)
def add_thumbnail(sender, instance, created, *args, **kwargs):
    '''
    Add a thumbnail image to the Image model after it is saved to DB
    '''
    if created:
        image = img.open(instance.image_file.path)
        # Transpose Exif tags if the image has them
        try:
            image = ImageOps.exif_transpose(image)
            image.save(q)
        except:
            pass
        max_size = (250, 250)
        image.thumbnail(max_size)
        thumb_dir = instance.creation_date.strftime(
            'member_{0}/thumbnails/%Y/%m/%d/{1}'.format(instance.member.pk)
        )
        file_name = instance.image_file.name.split('/')[-1].split('.')[0]
        extension = instance.image_file.name.split('/')[-1].split('.')[-1]
        thumb_file_name = '{}{}{}'.format(file_name, '-thumbnail.', extension)
        p = Path('media')
        q = p / thumb_dir
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
def add_thumbnail(sender, instance, *args **kwargs):
    '''
    Remove image files related to the deleted Image instance from the filesystem
    '''
    if instance.image_file:
        _delete_file(instance.image_file.path)
    if instance.thumbnail_file:
        _delete_file(instance.thumbnail_file.path)

