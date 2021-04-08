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
        'responses/', 
        views.ResponsePostListView.as_view(),
        name='public_responses',
    ),
    path(
        'responses/top/', 
        views.TopResponsePostListView.as_view(),
        name='top_responses',
    ),
    path(
        'reports/', 
        views.ReportPostListView.as_view(),
        name='reports',
    ),
    path(
        '<slug:slug>/', 
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
    path(
        'responses/<slug:slug>/', 
        views.ResponsePostDetailView.as_view(),
        name='response_detail',
    ),
    path(
        'reports/<int:pk>/', 
        views.ReportPostDetailView.as_view(),
        name='report_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/', 
        views.MemberPostView.as_view(),
        name='member_posts',
    ),
    path(
        'responses/member/<slug:member>/', 
        views.MemberResponsePostView.as_view(),
        name='member_responses',
    ),
    path(
        'reports/member/<slug:member>/', 
        views.MemberReportPostView.as_view(),
        name='member_reports',
    ),
    # Create Views
    path(
        'add/post/', 
        views.PostCreateView.as_view(),
        name='post_create',
    ),
    path(
        'add/response/', 
        views.ResponsePostCreateView.as_view(),
        name='responsepost_create',
    ),
    path(
        'add/report/', 
        views.ReportPostCreateView.as_view(),
        name='post_create',
    ),
    # Update Views
    path(
        'modify/post/<slug:slug>/', 
        views.PostUpdateView.as_view(),
        name='post_update',
    ),
    path(
        'modify/response/<slug:slug>/', 
        views.ResponsePostUpdateView.as_view(),
        name='post_update',
    ),
    # Delete Views
    path(
        'delete/post/<int:pk>/', 
        views.PostDeleteView.as_view(),
        name='post_delete',
    ),
    path(
        'delete/response/<int:pk>/', 
        views.ResponsePostDeleteView.as_view(),
        name='response_delete',
    ),
    path(
        'delete/report/<int:pk>/', 
        views.ResponsePostDeleteView.as_view(),
        name='report_delete',
    ),
    # Publish Views
    path(
        'publish/post/<int:pk>/', 
        views.publish_post_view,
        name='publish_post',
    ),
    path(
        'publish/response/<int:pk>/', 
        views.publish_responsepost_view,
        name='publish_response',
    ),
    # Marshmallow Views
    path(
        '<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_post_view,
        name='post_marshmallow',
    ),
    path(
        'responses/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_responsepost_view,
        name='response_marshmallow',
    ),
]
