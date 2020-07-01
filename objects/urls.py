from django.urls import path
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
import objects.views as views  

app_name = 'objects'

urlpatterns = [
    # Read Views
    path(
        'images/',
        views.ImageListView.as_view(),
        name='public_images',
    ),
    path(
        'images/<int:pk>/',
        views.ImageDetailView.as_view(),
        name='image_detail',
    ),
    path(
        'sounds/',
        views.SoundListView.as_view(),
        name='public_sounds',
    ),
    path(
        'sounds/<int:pk>/',
        views.SoundDetailView.as_view(),
        name='sound_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/images/',
        views.MemberImageView.as_view(),
        name='member_images',
    ),
    path(
        'member/<slug:member>/sounds/',
        views.MemberImageView.as_view(),
        name='member_sounds',
    ),
    # Create Views
    path(
        'upload/image/',
        views.ImageCreateView.as_view(),
        name='image_create',
    ),
    path(
        'upload/sound/',
        views.SoundCreateView.as_view(),
        name='sound_create',
    ),
    # Update Views
    path(
        'modify/image/<int:pk>',
        views.ImageUpdateView.as_view(),
        name='image_update',
    ),
    path(
        'modify/sound/<int:pk>',
        views.SoundUpdateView.as_view(),
        name='sound_update',
    ),
    # Delete Views
    path(
        'delete/image/<int:pk>',
        views.ImageDeleteView.as_view(),
        name='image_delete',
    ),
    path(
        'delete/sound/<int:pk>',
        views.SoundDeleteView.as_view(),
        name='sound_delete',
    ),
    # Publish Views
    path(
        'publish/sound/<int:pk>',
        views.publish_sound_view,
        name='publish_sound',
    ),
]
