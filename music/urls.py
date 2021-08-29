from django.urls import path
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
import music.views as views  

app_name = 'music'

urlpatterns = [
    # Music landing page
    path(
        '',
        views.MusicPageView.as_view(),
        name="music_page",
    ),
    # Music app profile
    ## Update
    path(
        'profile/update/<int:pk>/', 
        views.MusicAppProfileUpdateView.as_view(),
        name='music_app_profile_update',
    ),
    # Music landing page section views
    ## Create
    path(
        'add/section/', 
        views.MusicPageSectionCreateView.as_view(),
        name='music_page_section_create',
    ),
    ## Detail
    path(
        'sections/<int:pk>/',
        views.MusicPageSectionDetailView.as_view(),
        name='music_page_section_detail',
    ),
    ## Update
    path(
        'update/section/<int:pk>/', 
        views.MusicPageSectionUpdateView.as_view(),
        name='music_page_section_update',
    ),
    ## Delete
    path(
        'delete/section/<int:pk>/',
        views.MusicPageSectionDeleteView.as_view(),
        name='music_page_section_delete',
    ),
    # Read Views
    path(
        'albums/new/',
        views.AlbumListView.as_view(),
        name='new_albums',
    ),
    path(
        'albums/',
        views.TopAlbumListView.as_view(),
        name='top_albums',
    ),
    path(
        'albums/<slug:slug>/',
        views.AlbumDetailView.as_view(),
        name='album_detail',
    ),
    path(
        'tracks/new/',
        views.TrackListView.as_view(),
        name='new_tracks',
    ),
    path(
        'tracks/',
        views.TopTrackListView.as_view(),
        name='top_tracks',
    ),
    path(
        'tracks/<slug:slug>/',
        views.TrackDetailView.as_view(),
        name='track_detail',
    ),
    path(
        'member/<slug:member>/albums/',
        views.MemberAlbumView.as_view(),
        name='member_albums',
    ),
    path(
        'studio/albums/',
        views.AlbumStudioListView.as_view(),
        name='album_studio_list',
    ),
    path(
        'member/<slug:member>/tracks/',
        views.MemberTrackView.as_view(),
        name='member_tracks',
    ),
    path(
        'studio/tracks/',
        views.TrackStudioListView.as_view(),
        name='track_studio_list',
    ),
    # Create Views
    path(
        'add/album/',
        views.AlbumCreateView.as_view(),
        name='album_create',
    ),
    path(
        'add/track/',
        views.TrackCreateView.as_view(),
        name='track_create',
    ),
    # Update Views
    path(
        'modify/album/<slug:slug>/',
        views.AlbumUpdateView.as_view(),
        name='album_update',
    ),
    path(
        'modify/track/<slug:slug>/',
        views.TrackUpdateView.as_view(),
        name='track_update',
    ),
    # Delete Views
    path(
        'delete/album/<int:pk>/',
        views.AlbumDeleteView.as_view(),
        name='album_delete',
    ),
    path(
        'delete/track/<int:pk>/',
        views.TrackDeleteView.as_view(),
        name='track_delete',
    ),
    # Publish Views
    path(
        'publish/album/<int:pk>/',
        views.publish_album_view,
        name='publish_album',
    ),
    path(
        'publish/track/<int:pk>/',
        views.publish_track_view,
        name='publish_track',
    ),
    # Marshmallow Views
    path(
        'albums/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_album_view,
        name='album_marshmallow',
    ),
    path(
        'tracks/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_track_view,
        name='track_marshmallow',
    ),
]
