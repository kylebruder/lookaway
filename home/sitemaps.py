from django.contrib.sitemaps import Sitemap
from art.models import Gallery, Visual
from documentation.models import Article, Story, SupportDocument
from music.models import Album, Track
from posts.models import Post


class GallerySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Gallery.objects.filter(
            is_public=True,
        )

    def lastmod(self, obj):
        return obj.publication_date

class VisualSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Visual.objects.filter(
            is_public=True,
        )

    def lastmod(self, obj):
        return obj.publication_date

class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Article.objects.filter(
            is_public=True,
        )

    def lastmod(self, obj):
        return obj.publication_date

class StorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Story.objects.filter(
            is_public=True,
        )

    def lastmod(self, obj):
        return obj.publication_date

class SupportDocumentSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return SupportDocument.objects.filter(
            is_public=True,
        )

    def lastmod(self, obj):
        return obj.publication_date

class AlbumSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Album.objects.filter(
            is_public=True,
        )

    def lastmod(self, obj):
        return obj.publication_date

class TrackSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Track.objects.filter(
            is_public=True,
        )

    def lastmod(self, obj):
        return obj.publication_date

class PostsSitemap(Sitemap):
    changefreq = "hourly"
    priority = 0.5

    def items(self):
        return Post.objects.filter(
            is_public=True,
            members_only=False,
        )

    def lastmod(self, obj):
        return obj.publication_date

whole_site = {
    'galleries': GallerySitemap,
    'visuals': VisualSitemap,
    'articles': ArticleSitemap,
    'stories': StorySitemap,
    'information': SupportDocumentSitemap,
    'albums': AlbumSitemap,
    'tracks': TrackSitemap,
}
