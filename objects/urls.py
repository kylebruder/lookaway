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
    path(
        'code/',
        views.CodeListView.as_view(),
        name='public_code',
    ),
    path(
        'code/<int:pk>/',
        views.CodeDetailView.as_view(),
        name='code_detail',
    ),
    path(
        'links/',
        views.LinkListView.as_view(),
        name='public_links',
    ),
    path(
        'links/<int:pk>/',
        views.LinkDetailView.as_view(),
        name='link_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/images/',
        views.MemberImageView.as_view(),
        name='member_images',
    ),
    path(
        'member/<slug:member>/sounds/',
        views.MemberSoundView.as_view(),
        name='member_sounds',
    ),
    path(
        'member/<slug:member>/code/',
        views.MemberCodeView.as_view(),
        name='member_code',
    ),
    path(
        'member/<slug:member>/link/',
        views.MemberLinkView.as_view(),
        name='member_links',
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
    path(
        'upload/code/',
        views.CodeCreateView.as_view(),
        name='code_create',
    ),
    path(
        'upload/link/',
        views.LinkCreateView.as_view(),
        name='link_create',
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
    path(
        'modify/code/<int:pk>',
        views.CodeUpdateView.as_view(),
        name='code_update',
    ),
    path(
        'modify/link/<int:pk>',
        views.LinkUpdateView.as_view(),
        name='link_update',
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
    path(
        'delete/code/<int:pk>',
        views.CodeDeleteView.as_view(),
        name='code_delete',
    ),
    path(
        'delete/link/<int:pk>',
        views.LinkDeleteView.as_view(),
        name='link_delete',
    ),
    # Publish Views
    path(
        'publish/image/<int:pk>',
        views.publish_image_view,
        name='publish_image',
    ),
    path(
        'publish/sound/<int:pk>',
        views.publish_sound_view,
        name='publish_sound',
    ),
    path(
        'publish/code/<int:pk>',
        views.publish_code_view,
        name='publish_code',
    ),
    path(
        'publish/link/<int:pk>',
        views.publish_link_view,
        name='publish_link',
    ),
]