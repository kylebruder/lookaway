from django.urls import path
import documentation.views as views

app_name= "documentation"

urlpatterns = [
    # Read Views
    path(
        '', 
        views.DocumentListView.as_view(),
        name='public_documents',
    ),
    path(
        'documents/<slug:slug>/', 
        views.DocumentDetailView.as_view(),
        name='document_detail',
    ),
    path(
        'document-section/<int:pk>/', 
        views.DocumentSectionDetailView.as_view(),
        name='document_section_detail',
    ),
    path(
        'support/', 
        views.SupportDocumentListView.as_view(),
        name='public_support_documents',
    ),
    path(
        'support/<slug:slug>/', 
        views.SupportDocumentDetailView.as_view(),
        name='support_document_detail',
    ),
    path(
        'support-doc-section/<int:pk>/', 
        views.SupportDocSectionDetailView.as_view(),
        name='support_doc_section_detail',
    ),
    # Member Specific Views
    path(
        'member/<slug:member>/documents/', 
        views.MemberDocumentView.as_view(),
        name='member_documents',
    ),
    path(
        'member/<slug:member>/document-sections/', 
        views.MemberDocumentSectionView.as_view(),
        name='member_support_doc_section',
    ),
    path(
        'member/<slug:member>/support-documents/', 
        views.MemberSupportDocumentView.as_view(),
        name='member_support_documents',
    ),
    path(
        'member/<slug:member>/support-doc-sections/', 
        views.MemberSupportDocSectionView.as_view(),
        name='member_support_doc_section',
    ),
    # Create Views
    path(
        'add/document/', 
        views.DocumentCreateView.as_view(),
        name='document_create',
    ),
    path(
        'add/document-section/', 
        views.DocumentSectionCreateView.as_view(),
        name='document_section_create',
    ),
    path(
        'add/support-document/', 
        views.SupportDocumentCreateView.as_view(),
        name='support_document_create',
    ),
    path(
        'add/support-doc-section/', 
        views.SupportDocSectionCreateView.as_view(),
        name='support_doc_section_create',
    ),
    # Update Views
    path(
        'modify/document/<slug:slug>/', 
        views.DocumentUpdateView.as_view(),
        name='document_update',
    ),
    path(
        'modify/document-section/<int:pk>/', 
        views.DocumentSectionUpdateView.as_view(),
        name='document_section_update',
    ),
    path(
        'modify/support-document/<slug:slug>/', 
        views.SupportDocumentUpdateView.as_view(),
        name='support_document_update',
    ),
    path(
        'modify/support-doc-section/<int:pk>/', 
        views.SupportDocSectionUpdateView.as_view(),
        name='support_doc_section_update',
    ),
    # Delete Views
    path(
        'delete/document/<int:pk>/', 
        views.DocumentDeleteView.as_view(),
        name='document_delete',
    ),
    path(
        'delete/document-section/<int:pk>/', 
        views.DocumentSectionDeleteView.as_view(),
        name='document_section_delete',
    ),
    path(
        'delete/support-document/<int:pk>/', 
        views.SupportDocumentDeleteView.as_view(),
        name='support_document_delete',
    ),
    path(
        'delete/support-doc-section/<int:pk>/', 
        views.SupportDocSectionDeleteView.as_view(),
        name='support_doc_section_delete',
    ),
    # Publish Views
    path(
        'publish/document/<int:pk>/', 
        views.publish_document_view,
        name='publish_document',
    ),
    path(
        'publish/support-document/<int:pk>/', 
        views.publish_support_document_view,
        name='publish_support_document',
    ),
    # Marshmallow Views
    path(
        'document/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_document_view,
        name='document_marshmallow',
    ),
    path(
        'support-document/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_support_document_view,
        name='support_document_marshmallow',
    ),
]
