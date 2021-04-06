from django.urls import path
import posts.views as views

app_name= "posts"

urlpatterns = [
    # Posts landing page
    path(
        '',
        views.PostsPageView.as_view(),
        name="posts_page",
    ),
    # Posts app profile
    ## Update
    path(
        'profile/update/<int:pk>/',
        views.PostsAppProfileUpdateView.as_view(),
        name='posts_app_profile_update',
    ),
    # Posts landing page section views
    ## Create
    path(
        'add/section/',
        views.PostsPageSectionCreateView.as_view(),
        name='posts_page_section_create',
    ),
    ## Detail
    path(
        'sections/<int:pk>/',
        views.PostsPageSectionDetailView.as_view(),
        name='posts_page_section_detail',
    ),
    ## Update
    path(
        'update/section/<int:pk>/',
        views.PostsPageSectionUpdateView.as_view(),
        name='posts_page_section_update',
    ),
    ## Delete
    path(
        'delete/section/<int:pk>/',
        views.PostsPageSectionDeleteView.as_view(),
        name='posts_page_section_delete',
    ),
    # Read Views
    path(
        '', 
        views.PostListView.as_view(),
        name='public_posts',
    ),
    path(
        'top/', 
        views.TopPostListView.as_view(),
        name='top_posts',
    ),
    path(
        '', 
        views.PostResponseListView.as_view(),
        name='public_responses',
    ),
    path(
        'top/', 
        views.TopPostResponseListView.as_view(),
        name='top_responses',
    ),
    path(
        '<slug:slug>/', 
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/', 
        views.MemberPostView.as_view(),
        name='member_posts',
    ),
    # Create Views
    path(
        'add/post/', 
        views.PostCreateView.as_view(),
        name='post_create',
    ),
    # Update Views
    path(
        'modify/post/<slug:slug>/', 
        views.PostUpdateView.as_view(),
        name='post_update',
    ),
    # Delete Views
    path(
        'delete/post/<int:pk>/', 
        views.PostDeleteView.as_view(),
        name='post_delete',
    ),
    # Publish Views
    path(
        'publish/post/<int:pk>/', 
        views.publish_post_view,
        name='publish_post',
    ),
    # Marshmallow Views
    path(
        '<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_post_view,
        name='post_marshmallow',
    ),
]
