"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path

from .custom_site import custom_site
from appBlog.views import IndexView, CategoryView, TagView, ArticleDetailView, SearchView, AuthorView
from appConfig.views import LinkListView
from appComment.views import CommentView
from appBlog.rss import LatestArticleFeed
from appBlog.sitemap import ArticleSitemap


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('category/<int:category_id>', CategoryView.as_view(), name="category-list"),
    path('tag/<int:tag_id>', TagView.as_view(), name="tag-list"),
    path('article/<int:article_id>.html', ArticleDetailView.as_view(), name="article-detail"),
    path('search', SearchView.as_view(), name="search"),
    path('author/<int:owner_id>', AuthorView.as_view(), name="author-list"),
    path('link', LinkListView.as_view(), name="links-list"),
    path('comment', CommentView.as_view(), name='comment'),
    path('rss', LatestArticleFeed(), name='rss'),
    path('sitemap.xml', sitemap_views.sitemap, {'sitemaps': {'article': ArticleSitemap}}),
    path('super_admin', admin.site.urls, name="super-admin"),
    path('admin', custom_site.urls, name="admin"),
]
