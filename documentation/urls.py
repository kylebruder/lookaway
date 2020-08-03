from django.urls import path
import documentation.views as views

app_name= "documentation"

urlpatterns = [
    # Read Views
    path(
        '', 
        views.SupportDocumentListView.as_view(),
        name='public_support_documents',
    ),
    path(
        '<slug:slug>/', 
        views.SupportDocumentDetailView.as_view(),
        name='support_document_detail',
    ),
    path(
        'section/<int:pk>/', 
        views.SectionDetailView.as_view(),
        name='section_document_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/', 
        views.SupportDocumentListView.as_view(),
        name='member_support_documents',
    ),
    # Create Views
    path(
        'add/support-document/', 
        views.SupportDocumentCreateView.as_view(),
        name='support_document_create',
    ),
    path(
        'add/section/', 
        views.SectionCreateView.as_view(),
        name='section_create',
    ),
    # Update Views
    path(
        'modify/support-document/', 
        views.SupportDocumentUpdateView.as_view(),
        name='support_document_update',
    ),
    path(
        'modify/section/', 
        views.SectionUpdateView.as_view(),
        name='section_update',
    ),
    # Delete Views
    path(
        'delete/support-document/', 
        views.SupportDocumentDeleteView.as_view(),
        name='support_document_delete',
    ),
    path(
        'delete/section/', 
        views.SectionDeleteView.as_view(),
        name='section_delete',
    ),
    # Publish Views
    path(
        'publish/support-document/', 
        views.publish_support_document_view,
        name='publish_support_document',
    ),
]
