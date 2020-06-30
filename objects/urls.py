from django.urls import path
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from .views import (ImageCreateView, ImageListView, MemberImageView, 
    ImageDetailView, ImageUpdateView, ImageDeleteView, publish_image_view)

app_name = 'objects'

urlpatterns = [
    path(
        'images/',
        ImageListView.as_view(),
        name='public_images',
    ),
    path(
        'images/<int:pk>/',
        ImageDetailView.as_view(),
        name='image_detail',
    ),
    path(
        'member/<slug:member>/images/',
        MemberImageView.as_view(),
        name='member_images',
    ),
    path(
        'upload/image/',
        ImageCreateView.as_view(),
        name='image_create',
    ),
    path(
        'modify/image/<int:pk>',
        ImageUpdateView.as_view(),
        name='image_update',
    ),
    path(
        'delete/image/<int:pk>',
        ImageDeleteView.as_view(),
        name='image_delete',
    ),
    path(
        'publish/image/<int:pk>',
        publish_image_view,
        name='publish_image',
    ),
]
