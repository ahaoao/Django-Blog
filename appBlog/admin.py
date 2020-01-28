from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Category, Tag, Article
from .adminforms import ArticleAdminForm
from Blog.custom_site import custom_site
from Blog.base_admin import BaseOwnerAdmin


# Register your models here.
@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    """分类管理类"""
    # 显示页展示的数据
    list_display = ('name', 'status', 'is_nav', 'owner', 'article_count', 'created_time')
    # 表单页展示的数据
    fields = ('name', 'status', 'is_nav')

    # # 重写save_model获取当前登陆的数据
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user  # 设置owner为当前用户
    #     return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def article_count(self, obj):
        # 文章数量
        return obj.article_set.count()

    article_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    """标签管理类"""
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户的分类"""
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Article, site=custom_site)
class ArticleAdmin(BaseOwnerAdmin):
    """文章管理类"""
    form = ArticleAdminForm

    list_display = ('title', 'category', 'status', 'owner', 'created_time', 'operator')
    list_display_links = []
    list_filter = (CategoryOwnerFilter, )

    search_fields = ('title', 'category__name', )

    # 动作相关的配置，是否显示在顶部和底部
    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True  # 将操作按钮同时显示在顶部
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': ('title', 'category', 'status'),
        }),
        ('内容', {
            'fields': ('desc', 'content', ),
        }),
        ('额外信息', {
            'classes': ('collapse', ),
            'fields': ('tag', ),
        })
    )

    # 自定义操作字段
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:appBlog_article_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(ArticleAdmin, self).save_model(request, obj, form, change)
    #
    # # 自定义显示页字段 仅显示当前账号发表的文章
    # def get_queryset(self, request):
    #     qs = super(ArticleAdmin, self).get_queryset(request)
    #     return qs.filter(owner=request.user)

    # class Media:
    #     css = {
    #         'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
    #     }
    #     js = ('https://chn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    """日志记录"""
    list_display = ('object_repr', 'object_id', 'action_flag', 'user', 'change_message')





















