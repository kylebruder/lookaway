from django.urls import path
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
import art.views as views

app_name = 'art'

urlpatterns = [
    # Music front page
    path(
        '',
        views.ArtPageView.as_view(),
        name="art_page",
    ),
    # Read Views
    path(
        'galleries/new/',
        views.GalleryListView.as_view(),
        name='new_galleries',
    ),
    path(
        'galleries/',
        views.TopGalleryListView.as_view(),
        name='top_galleries',
    ),
    path(
        'galleries/<slug:slug>/',
        views.GalleryDetailView.as_view(),
        name='gallery_detail',
    ),
    path(
        'visuals/new/',
        views.VisualListView.as_view(),
        name='new_visuals',
    ),
    path(
        'visuals/',
        views.TopVisualListView.as_view(),
        name='top_visuals',
    ),
    path(
        'visuals/<slug:slug>/',
        views.VisualDetailView.as_view(),
        name='visual_detail',
    ),
    path(
        'member/<slug:member>/galleries/',
        views.MemberGalleryView.as_view(),
        name='member_galleries',
    ),
    path(
        'member/<slug:member>/visuals/',
        views.MemberVisualView.as_view(),
        name='member_visuals',
    ),
    # Create Views
    path(
        'add/gallery/',
        views.GalleryCreateView.as_view(),
        name='gallery_create',
    ),
    path(
        'add/visual/',
        views.VisualCreateView.as_view(),
        name='visual_create',
    ),
    # Update Views
    path(
        'modify/gallery/<slug:slug>/',
        views.GalleryUpdateView.as_view(),
        name='gallery_update',
    ),
    path(
        'modify/visual/<slug:slug>/',
        views.VisualUpdateView.as_view(),
        name='visual_update',
    ),
    # Delete Views
    path(
        'delete/gallery/<slug:slug>/',
        views.GalleryDeleteView.as_view(),
        name='gallery_delete',
    ),
    path(
        'delete/visual/<slug:slug>/',
        views.VisualDeleteView.as_view(),
        name='visual_delete',
    ),
    # Publish Views
    path(
        'publish/gallery/<int:pk>/',
        views.publish_gallery_view,
        name='publish_gallery',
    ),
    path(
        'publish/visual/<int:pk>/',
        views.publish_visual_view,
        name='publish_visual',
    ),
    # Marshmallow Views
    path(
        'galleries/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_gallery_view,
        name='gallery_marshmallow',
    ),
    path(
        'visuals/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_visual_view,
        name='visual_marshmallow',
    ),
]
