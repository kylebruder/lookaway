from django.urls import path
import home.views as views

app_name = 'home'

urlpatterns = [
    # Landing page
    path('', views.IndexView.as_view(), name='index'),
    # Home app profile
    ## Update
    path(
        'profile/update/<int:pk>/site/settings/', 
        views.SiteProfileUpdateView.as_view(),
        name='site_profile_update',
    ),
    path(
        'profile/update/<int:pk>/', 
        views.HomeAppProfileUpdateView.as_view(),
        name='home_app_profile_update',
    ),
    path(
        'profile/update/<int:pk>/settings/', 
        views.HomeAppProfileSettingsUpdateView.as_view(),
        name='home_app_profile_settings_update',
    ),
    # Home landing page section views
    ## Create
    path(
        'add/section/', 
        views.HomePageSectionCreateView.as_view(),
        name='home_page_section_create',
    ),
    ## Detail
    path(
        'sections/<int:pk>/',
        views.HomePageSectionDetailView.as_view(),
        name='home_page_section_detail',
    ),
    ## Update
    path(
        'update/section/<int:pk>/', 
        views.HomePageSectionUpdateView.as_view(),
        name='home_page_section_update',
    ),
    ## Delete
    path(
        'delete/section/<int:pk>/',
        views.HomePageSectionDeleteView.as_view(),
        name='home_page_section_delete',
    ),
]
