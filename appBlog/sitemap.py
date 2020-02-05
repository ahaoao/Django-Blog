"""实现sitemap(站点地图) 主要用途提供给搜索引擎，有利于收录我们的网站"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article


class ArticleSitemap(Sitemap):
    changefreq = "always"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Article.objects.filter(status=Article.STATUS_NORMAL)

    def lastmod(self, obj):
        return obj.created_time

    def location(self, obj):
        return reverse('article-detail', args=[obj.pk])