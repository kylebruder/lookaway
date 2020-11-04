from django.urls import path
from django.contrib.auth import views as auth_views
from .views import StudioView, MemberListView, MemberProfileView, MemberProfileUpdateView, InviteLinkDetailView, member_registration

app_name = "members"
urlpatterns = [
    path(
        '', 
        MemberListView.as_view(),
        name='member_list',
    ),
    path(
        'studio/',
        StudioView.as_view(),
        name='studio',
    ),
    path(
        '<slug:slug>/', 
        MemberProfileView.as_view(),
        name='member_profile',
    ),
    path(
        '<slug:slug>/profile/', 
        MemberProfileUpdateView.as_view(),
        name='member_profile_update',
    ),
    path(
        'join-us/<slug:slug>/', 
        InviteLinkDetailView.as_view(),
        name='invite_link_detail',
    ),
    path(
        'register/<slug:invite>/', 
        member_registration,
        name='member_registration',
    ),
]
