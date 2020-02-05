"""实现RSS订阅器(简易信息聚合)"""

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Article


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestArticleFeed(Feed):
    feed_type = ExtendedRSSFeed  # 这里定制Rss。 可以不写feed_type，默认为Rss201rev2Feed，
    title = "Typeidea Blog System"
    link = "/rss/"
    description = "typeidea is a blog system power by django"

    def items(self):
        return Article.objects.filter(status=Article.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('article-detail', args=[item.pk])

    def item_extra_kwargs(self, item):
        return {'content_html': self.item_content_html(item)}

    def item_content_html(self, item):
        return item.content_html
