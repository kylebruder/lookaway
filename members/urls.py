from django.urls import path
from django.contrib.auth import views as auth_views
import members.views as views

app_name = "members"
urlpatterns = [
    # Members landing page
    path(
        '',
        views.MembersPageView.as_view(),
        name="members_page",
    ),
    # Members app profile
    ## Update
    path(
        'app-profile/update/<int:pk>/', 
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
    # Member profile
    ## Update
    path(
        'profile/update/<int:pk>/',
        views.MemberProfileUpdateView.as_view(),
        name='member_profile_update',
    ),
    path(
        'profile/settings/update/<int:pk>/',
        views.MemberProfileSettingsUpdateView.as_view(),
        name='member_profile_settings_update',
    ),
    # Member profile page section views
    ## Create
    path(
        'profile/add/section/',
        views.MemberProfileSectionCreateView.as_view(),
        name='member_profile_section_create',
    ),
    ## Detail
    path(
        'profile/sections/<int:pk>/',
        views.MemberProfileSectionDetailView.as_view(),
        name='member_profile_section_detail',
    ),
    ## Update
    path(
        'profile/update/section/<int:pk>/', 
        views.MemberProfileSectionUpdateView.as_view(),
        name='member_profile_section_update',
    ),
    ## Delete
    path(
        'profile/delete/section/<int:pk>/',
        views.MemberProfileSectionDeleteView.as_view(),
        name='member_profile_section_delete',
    ),
    ## List
    path(
        'all/', 
        views.MemberListView.as_view(),
        name='member_list',
    ),
    path(
        'contributors/', 
        views.ContributorListView.as_view(),
        name='contributor_list',
    ),
    path(
        'artists/', 
        views.ArtistListView.as_view(),
        name='artist_list',
    ),
    path(
        'musicians/', 
        views.MusicianListView.as_view(),
        name='musician_list',
    ),
    path(
        'writers/', 
        views.WriterListView.as_view(),
        name='writer_list',
    ),
    path(
        'staff/', 
        views.StaffListView.as_view(),
        name='staff_list',
    ),
    # Studio
    path(
        'studio/',
        views.StudioView.as_view(),
        name='studio',
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
    # Profile page
    path(
        '<slug:slug>/', 
        views.MemberProfileView.as_view(),
        name='member_profile',
    ),
]
