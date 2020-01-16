"""
评论相关的Model
"""

from django.db import models
from appBlog.models import Article


# Create your models here.
class Comment(models.Model):
    """评论表"""
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    target = models.ForeignKey(Article, verbose_name="评论目标", on_delete=models.CASCADE)
    content = models.TextField(max_length=2000, verbose_name="内容")
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    website = models.URLField(verbose_name="网站")
    email = models.EmailField(verbose_name="邮箱")
    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=STATUS_NORMAL, verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name_plural = "评论"