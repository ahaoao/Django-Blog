"""
配置相关的Model
"""

from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string


# Create your models here.
class Link(models.Model):
    """友链表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")  # 默认长度为200
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    weight = models.PositiveIntegerField(choices=zip(range(1, 6), range(1, 6) ), default=1, verbose_name="权重", help_text="权重高展示顺序靠前")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    @classmethod
    def get_normal(cls):
        """获取正常友链表"""
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    class Meta:
        verbose_name_plural = "友链"


class SideBar(models.Model):
    """侧边栏表"""
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )
    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4

    SIDE_TYPE = (
        (DISPLAY_HTML, 'HTML'),
        (DISPLAY_LATEST, '最新文章'),
        (DISPLAY_HOT, '最热文章'),
        (DISPLAY_COMMENT, '最近评论'),
    )
    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(choices=SIDE_TYPE, default=DISPLAY_HTML, verbose_name="展示类型")
    content = models.CharField(max_length=500,  blank=True, verbose_name="内容", help_text="如果设置的不是 HTML 类型，可以为空")
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_SHOW, verbose_name="状态")
    owner = models.ForeignKey(User, verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    class Meta:
        verbose_name_plural = "侧边栏"

    """
    封装SideBar到Model层
    """
    @property
    def content_html(self):
        """直接渲染模板"""
        from appBlog.models import Article
        from appComment.models import Comment

        result = ''

        if self.display_type == self.DISPLAY_HTML:  # HTML
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:  # 最新文章
            context = {
                'articles': Article.latest_articles()
            }
            result = render_to_string('appconfig/blocks/sidebar_articles.html', context)
        elif self.display_type == self.DISPLAY_HOT:  # 最热文章
            context = {
                'articles': Article.hot_article()
            }
            result = render_to_string('appconfig/blocks/sidebar_articles.html', context)
        elif self.display_type == self.DISPLAY_COMMENT:  # 最近评论
            context = {
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL).order_by('-id')[:5]  # 降序排列取前五条数据
            }
            result = render_to_string('appconfig/blocks/sidebar_comments.html', context)
        return result

