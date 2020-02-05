from datetime import date

from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.cache import cache

from .models import Tag, Article, Category
from appConfig.models import SideBar
# from appComment.forms import CommentForm
# from appComment.models import Comment


# Create your views here.
class CommonViewMixin:
    def get_context_data(self, **kwargs):
        """获取需要渲染到模板中的数据"""
        context = super().get_context_data(**kwargs)
        context.update({
            # 侧边栏的数据，在base.html中的sidebar.content_html(侧边栏模板渲染)是封装在Model层的
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    """首页视图"""
    queryset = Article.latest_articles()  # 按id降序的所有文章列表
    paginate_by = 10  # 设置每页展示的数据量
    template_name = 'appblog/list.html'  # 设置渲染的模板
    # 为get_queryset()返回的model列表重新命名，默认是object_list，这里重新命名为article_list
    context_object_name = 'article_list'


class ArticleDetailView(CommonViewMixin, DetailView):
    """文章细节视图"""
    queryset = Article.latest_articles()
    template_name = 'appblog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'
    # 抽象出评论组件后去掉get_context_data

    # 统计文章访问数量
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1*60)  # 1分钟有效
        if not cache.get(uv_key):
            increase_pv = True
            cache.set(uv_key, 1, 24*60*60)  # 24小时有效
        if increase_pv and increase_uv:
            Article.objects.filter(pk=self.object.id).update(pv=F('pv')+1, uv=F('uv')+1)
        elif increase_pv:
            Article.objects.filter(pk=self.object.id).update(pv=F('pv')+1)
        elif increase_uv:
            Article.objects.filter(pk=self.object.id).update(uv=F('uv')+1)


class CategoryView(IndexView):
    """分类页面视图"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')  # category_id是url定义中拿到的
        # 返回指定category_id的Category对象, 找到就返回，不存在就直接返回404错误
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据分类过滤"""
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')    # category_id是url定义中拿到的
        return queryset.filter(category_id=category_id)  # category_id是article里面存在的字段


class TagView(IndexView):
    """标签页面视图"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')  # tag_id是从url定义中拿到的
        tag = get_object_or_404(Tag, pk=tag_id)  # 获取一个对象的实例，如果获取到就返回实例对象，如果不存在直接抛出404错误
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        """重写queryset，根据标签过滤"""
        queryset = super().get_queryset()  # 继承IndexView的所有queryset(按id降序的所有文章列表)
        tag_id = self.kwargs.get('tag_id')  # tag_id是从url定义中拿到的
        return queryset.filter(tag__id=tag_id)  # ???????


class SearchView(IndexView):
    """查询页面视图"""
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')  # keyword为html的name属性
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        # 根据标题和摘要查询
        queryset = queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
        return queryset


class AuthorView(IndexView):
    """作者页面视图"""
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)

