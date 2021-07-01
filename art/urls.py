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
    # Art app profile
    ## Update
    path(
        'profile/update/<int:pk>/', 
        views.ArtAppProfileUpdateView.as_view(),
        name='art_app_profile_update',
    ),
    # Art landing page section views
    ## Create
    path(
        'add/section/', 
        views.ArtPageSectionCreateView.as_view(),
        name='art_page_section_create',
    ),
    ## Detail
    path(
        'sections/<int:pk>/', 
        views.ArtPageSectionDetailView.as_view(),
        name='art_page_section_detail',
    ),
    ## Update
    path(
        'update/section/<int:pk>/', 
        views.ArtPageSectionUpdateView.as_view(),
        name='art_page_section_update',
    ),
    ## Delete
    path(
        'delete/section/<int:pk>/', 
        views.ArtPageSectionDeleteView.as_view(),
        name='art_page_section_delete',
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
        'delete/gallery/<int:pk>/',
        views.GalleryDeleteView.as_view(),
        name='gallery_delete',
    ),
    path(
        'delete/visual/<int:pk>/',
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
