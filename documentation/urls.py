from django.urls import path
import documentation.views as views

app_name= "documentation"

urlpatterns = [
    # Documentation landing page
    path(
        '', 
        views.DocumentationPageView.as_view(),
        name='documentation_page',
    ),
    # Documentation app profile
    ## Update
    path(
        'profile/update/<int:pk>/', 
        views.DocumentationAppProfileUpdateView.as_view(),
        name='documentation_app_profile_update',
    ),
    # Documentation landing page section views
    ## Create
    path(
        'add/section/', 
        views.DocumentationPageSectionCreateView.as_view(),
        name='documentation_page_section_create',
    ),
    ## Detail
    path(
        'sections/<int:pk>/', 
        views.DocumentationPageSectionDetailView.as_view(),
        name='documentation_page_section_detail',
    ),
    ## Update
    path(
        'update/section/<int:pk>/', 
        views.DocumentationPageSectionUpdateView.as_view(),
        name='documentation_page_section_update',
    ),
    ## Delete
    path(
        'delete/section/<int:pk>/', 
        views.DocumentationPageSectionDeleteView.as_view(),
        name='documentation_page_section_delete',
    ),
    
    # Read views
    ## Article list views
    path(
        'articles/new/', 
        views.ArticleListView.as_view(),
        name='new_articles',
    ),
    path(
        'articles', 
        views.TopArticleListView.as_view(),
        name='top_articles',
    ),
    ## Article detail views
    path(
        'articles/<slug:slug>/', 
        views.ArticleDetailView.as_view(),
        name='article_detail',
    ),
    path(
        'article-section/<int:pk>/', 
        views.ArticleSectionDetailView.as_view(),
        name='article_section_detail',
    ),
    ## Story list views
    path(
        'stories/new/', 
        views.StoryListView.as_view(),
        name='new_stories',
    ),
    path(
        'stories/', 
        views.TopStoryListView.as_view(),
        name='top_stories',
    ),
    ## Story detail views
    path(
        'stories/<slug:slug>/', 
        views.StoryDetailView.as_view(),
        name='story_detail',
    ),
    path(
        'stories/story-section/<int:pk>/', 
        views.StorySectionDetailView.as_view(),
        name='story_section_detail',
    ),
    ## SupportDocument list views
    path(
        'information/new', 
        views.SupportDocumentListView.as_view(),
        name='new_support_documents',
    ),
    path(
        'information/', 
        views.TopSupportDocumentListView.as_view(),
        name='top_support_documents',
    ),
    ## SupportDocument detail views
    path(
        'information/<slug:slug>/', 
        views.SupportDocumentDetailView.as_view(),
        name='support_document_detail',
    ),
    path(
        'support-doc-section/<int:pk>/', 
        views.SupportDocSectionDetailView.as_view(),
        name='support_doc_section_detail',
    ),
    # Member specific views
    ## Member Articles
    path(
        'member/<slug:member>/articles/', 
        views.MemberArticleView.as_view(),
        name='member_articles',
    ),
    ## Member Stories
    path(
        'member/<slug:member>/stories/', 
        views.MemberStoryView.as_view(),
        name='member_stories',
    ),
    ## Member SupportDocuments
    path(
        'member/<slug:member>/information/', 
        views.MemberSupportDocumentView.as_view(),
        name='member_support_documents',
    ),
    # Create Views
    ## Article create views
    path(
        'add/article/', 
        views.ArticleCreateView.as_view(),
        name='article_create',
    ),
    path(
        'add/article-section/', 
        views.ArticleSectionCreateView.as_view(),
        name='article_section_create',
    ),
    ## Story create views
    path(
        'add/story/', 
        views.StoryCreateView.as_view(),
        name='story_create',
    ),
    path(
        'add/story-section/', 
        views.StorySectionCreateView.as_view(),
        name='story_section_create',
    ),
    ## SupportDocument create views
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
    ## Article update views
    path(
        'modify/article/<slug:slug>/', 
        views.ArticleUpdateView.as_view(),
        name='article_update',
    ),
    path(
        'modify/article-section/<int:pk>/', 
        views.ArticleSectionUpdateView.as_view(),
        name='article_section_update',
    ),
    ## Story update views
    path(
        'modify/story/<slug:slug>/', 
        views.StoryUpdateView.as_view(),
        name='story_update',
    ),
    path(
        'modify/story-section/<int:pk>/', 
        views.StorySectionUpdateView.as_view(),
        name='story_section_update',
    ),
    ## SupportDocument update views
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
    ## Article delete views
    path(
        'delete/article/<int:pk>/', 
        views.ArticleDeleteView.as_view(),
        name='article_delete',
    ),
    path(
        'delete/article-section/<int:pk>/', 
        views.ArticleSectionDeleteView.as_view(),
        name='article_section_delete',
    ),
    ## Story delete views
    path(
        'delete/story/<int:pk>/', 
        views.StoryDeleteView.as_view(),
        name='story_delete',
    ),
    path(
        'delete/story-section/<int:pk>/', 
        views.StorySectionDeleteView.as_view(),
        name='story_section_delete',
    ),
    ## SupportDocument delete views
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
    ## Article publish views
    path(
        'publish/article/<int:pk>/', 
        views.publish_article_view,
        name='publish_article',
    ),
    ## Story publish views
    path(
        'publish/story/<int:pk>/', 
        views.publish_story_view,
        name='publish_story',
    ),
    ## SupportDocument publish views
    path(
        'publish/support-document/<int:pk>/', 
        views.publish_support_document_view,
        name='publish_support_document',
    ),
    # Marshmallow Views
    ## Article marshmallow views
    path(
        'article/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_article_view,
        name='article_marshmallow',
    ),
    ## Story marshmallow views
    path(
        'story/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_story_view,
        name='story_marshmallow',
    ),
    ## SupportDocument marshmallow views
    path(
        'support-document/<int:pk>/add-marshmallow', 
        views.add_marshmallow_to_support_document_view,
        name='support_document_marshmallow',
    ),
]
