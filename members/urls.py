from django.urls import path
from django.contrib.auth import views as auth_views
from .views import StudioView, MemberProfileView, MemberProfileUpdateView

app_name = "members"

urlpatterns = [
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
]
