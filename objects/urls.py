from django.urls import path
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
import objects.views as views  

app_name = 'objects'

urlpatterns = [
    # Landing page
    path('', views.ObjectsPageView.as_view(), name='objects_page'),

    # Home app profile
    ## Update
    path(
        'profile/update/<int:pk>/transcoder/settings/', 
        views.ObjectsAppTranscoderSettingsUpdateView.as_view(),
        name='objects_app_transcoder_settings_update',
    ),
    path(
        'profile/update/<int:pk>/', 
        views.ObjectsAppProfileUpdateView.as_view(),
        name='objects_app_profile_update',
    ),
    # Home landing page section views
    ## Create
    path(
        'add/section/', 
        views.ObjectsPageSectionCreateView.as_view(),
        name='objects_page_section_create',
    ),
    ## Detail
    path(
        'sections/<int:pk>/',
        views.ObjectsPageSectionDetailView.as_view(),
        name='objects_page_section_detail',
    ),
    ## Update
    path(
        'update/section/<int:pk>/', 
        views.ObjectsPageSectionUpdateView.as_view(),
        name='objects_page_section_update',
    ),
    ## Delete
    path(
        'delete/section/<int:pk>/',
        views.ObjectsPageSectionDeleteView.as_view(),
        name='objects_page_section_delete',
    ),

    # Multimedia objects
    ## Read views
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
        'videos/',
        views.VideoListView.as_view(),
        name='public_videos',
    ),
    path(
        'videos/<int:pk>/',
        views.VideoDetailView.as_view(),
        name='video_detail',
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
    path(
        'tags/',
        views.TagListView.as_view(),
        name='tags',
    ),
    path(
        'tags/<slug:slug>/',
        views.TagDetailView.as_view(),
        name='tag_detail',
    ),
    path(
        'tags/get-tag-detail',
        views.get_tag_detail,
        name='get_tag_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/images/',
        views.MemberImageView.as_view(),
        name='member_images',
    ),
    path(
        'studio/images/',
        views.ImageStudioListView.as_view(),
        name='image_studio_list',
    ),
    path(
        'member/<slug:member>/sounds/',
        views.MemberSoundView.as_view(),
        name='member_sounds',
    ),
    path(
        'studio/sounds/',
        views.SoundStudioListView.as_view(),
        name='sound_studio_list',
    ),
    path(
        'member/<slug:member>/videos/',
        views.MemberVideoView.as_view(),
        name='member_videos',
    ),
    path(
        'studio/videos/',
        views.VideoStudioListView.as_view(),
        name='video_studio_list',
    ),
    path(
        'member/<slug:member>/code/',
        views.MemberCodeView.as_view(),
        name='member_code',
    ),
    path(
        'studio/code/',
        views.CodeStudioListView.as_view(),
        name='code_studio_list',
    ),
    path(
        'member/<slug:member>/links/',
        views.MemberLinkView.as_view(),
        name='member_links',
    ),
    path(
        'studio/links/',
        views.LinkStudioListView.as_view(),
        name='link_studio_list',
    ),
    # Create Views
    path(
        'add/image/',
        views.ImageCreateView.as_view(),
        name='image_create',
    ),
    path(
        'add/sound/',
        views.SoundCreateView.as_view(),
        name='sound_create',
    ),
    path(
        'add/video/',
        views.VideoCreateView.as_view(),
        name='video_create',
    ),
    path(
        'add/code/',
        views.CodeCreateView.as_view(),
        name='code_create',
    ),
    path(
        'add/link/',
        views.LinkCreateView.as_view(),
        name='link_create',
    ),
    path(
        'add/tag/',
        views.TagCreateView.as_view(),
        name='tag_create',
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
        'modify/video/<int:pk>',
        views.VideoUpdateView.as_view(),
        name='video_update',
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
    path(
        'modify/tag/<slug:slug>',
        views.TagUpdateView.as_view(),
        name='tag_update',
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
        'delete/video/<int:pk>',
        views.VideoDeleteView.as_view(),
        name='video_delete',
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
    path(
        'delete/tag/<slug:slug>',
        views.TagDeleteView.as_view(),
        name='tag_delete',
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
        'publish/video/<int:pk>',
        views.publish_video_view,
        name='publish_video',
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
    # Tag Views
    path(
        'tags/galleries/<slug:slug>',
        views.GalleryByTag.as_view(),
        name='gallery_tag',
    ),
    path(
        'tags/visuals/<slug:slug>',
        views.VisualByTag.as_view(),
        name='visual_tag',
    ),
    path(
        'tags/albums/<slug:slug>',
        views.AlbumByTag.as_view(),
        name='album_tag',
    ),
    path(
        'tags/tracks/<slug:slug>',
        views.TrackByTag.as_view(),
        name='track_tag',
    ),
    path(
        'tags/stories/<slug:slug>',
        views.StoryByTag.as_view(),
        name='story_tag',
    ),
    path(
        'tags/posts/<slug:slug>',
        views.PostByTag.as_view(),
        name='post_tag',
    ),
    path(
        'tags/articles/<slug:slug>',
        views.ArticleByTag.as_view(),
        name='article_tag',
    ),
    path(
        'tags/support-documents/<slug:slug>',
        views.SupportDocumentByTag.as_view(),
        name='support_document_tag',
    ),
    path(
        'tags/images/<slug:slug>',
        views.ImageByTag.as_view(),
        name='image_tag',
    ),
    path(
        'tags/sounds/<slug:slug>',
        views.SoundByTag.as_view(),
        name='sound_tag',
    ),
    path(
        'tags/videos/<slug:slug>',
        views.VideoByTag.as_view(),
        name='video_tag',
    ),
    path(
        'tags/code/<slug:slug>',
        views.CodeByTag.as_view(),
        name='code_tag',
    ),
    path(
        'tags/links/<slug:slug>',
        views.LinkByTag.as_view(),
        name='link_tag',
    ),
    # Marshmallow Views
    path(
        'images/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_image_view,
        name='image_marshmallow',
    ),
    path(
        'sounds/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_sound_view,
        name='sound_marshmallow',
    ),
    path(
        'videos/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_video_view,
        name='video_marshmallow',
    ),
    path(
        'code/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_code_view,
        name='code_marshmallow',
    ),
    path(
        'links/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_link_view,
        name='link_marshmallow',
    ),
    path(
        'tags/<int:pk>/add-marshmallow',
        views.add_marshmallow_to_tag_view,
        name='tag_marshmallow',
    ),
]
