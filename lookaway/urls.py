"""lookaway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import include, path
from members.views import InviteLinkCreateView, InviteLinkDetailView, MemberUpdateView
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'members/',
        include('members.urls'),
    ),
    path(
        'media/',
        include('objects.urls'),
    ),
    path(
        'documentation/',
        include('documentation.urls'),
    ),
    path(
        'posts/',
        include('posts.urls'),
    ),
    path(
        'music/',
        include('music.urls'),
    ),
    path(
        'art/',
        include('art.urls'),
    ),
    path(
        '',
        include('home.urls'),
    ),
    path(
        'invite/',
        InviteLinkCreateView.as_view(),
        name='invite',
    ),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='login.html'),
        name='login',
    ),
    path(
        'logout/',
         auth_views.LogoutView.as_view(),
         name='logout',
    ),
    path(
        'change-password/',
         auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change',
    ),
    path(
        'update-info/<int:pk>/',
         MemberUpdateView.as_view(),
         name='email_change',
    ),
    path(
        'reset-password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset',
    ),
    path(
        'reset-password-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset.html'),
         name='password_reset_confirm',
    ),
    path(
        'reset-password-done',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done',
    ),
    path(
        'reset-password-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete',
    ),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
