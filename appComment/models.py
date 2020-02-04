"""
评论相关的Model
"""

from django.db import models
from appBlog.models import Article


# Create your models here.
class Comment(models.Model):
    """评论表"""
    STATUS_DELETE = 0
    STATUS_NORMAL = 1
    STATUS_UNAUDITED = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_UNAUDITED, '未审核'),
    )
    # 评论目标的网址
    target = models.CharField(max_length=100, verbose_name="评论目标")
    content = models.TextField(max_length=2000, verbose_name="内容")
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    website = models.URLField(verbose_name="网站")
    email = models.EmailField(verbose_name="邮箱")
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_UNAUDITED, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.nickname

    @classmethod
    def get_by_target(cls, target):
        """返回target对象的有效评论"""
        return cls.objects.filter(target=target, status=cls.STATUS_NORMAL)

    class Meta:
        verbose_name_plural = "评论"
