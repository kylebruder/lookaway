from django.urls import path
import posts.views as views

app_name= "posts"

urlpatterns = [
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
