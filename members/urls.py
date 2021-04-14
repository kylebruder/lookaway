from django.urls import path
from django.contrib.auth import views as auth_views
import members.views as views

app_name = "members"
urlpatterns = [
    # Members app profile
    ## Update
    path(
        'profile/update/<int:pk>/', 
        views.MembersAppProfileUpdateView.as_view(),
        name='members_app_profile_update',
    ),
    # Members landing page section views
    ## Create
    path(
        'add/section/', 
        views.MembersPageSectionCreateView.as_view(),
        name='members_page_section_create',
    ),
    ## Detail
    path(
        'sections/<int:pk>/',
        views.MembersPageSectionDetailView.as_view(),
        name='members_page_section_detail',
    ),
    ## Update
    path(
        'update/section/<int:pk>/', 
        views.MembersPageSectionUpdateView.as_view(),
        name='members_page_section_update',
    ),
    ## Delete
    path(
        'delete/section/<int:pk>/',
        views.MembersPageSectionDeleteView.as_view(),
        name='members_page_section_delete',
    ),
    path(
        '', 
        views.MemberListView.as_view(),
        name='member_list',
    ),
    path(
        'studio/',
        views.StudioView.as_view(),
        name='studio',
    ),
    path(
        '<slug:slug>/', 
        views.MemberProfileView.as_view(),
        name='member_profile',
    ),
    path(
        '<slug:slug>/profile/', 
        views.MemberProfileUpdateView.as_view(),
        name='member_profile_update',
    ),
    path(
        'join-us/<slug:slug>/', 
        views.InviteLinkDetailView.as_view(),
        name='invite_link_detail',
    ),
    path(
        'register/<slug:invite>/', 
        views.member_registration,
        name='member_registration',
    ),
]
