from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Tag, Article, Category
from appConfig.models import SideBar, Link


# Create your views here.
class ArticleListView(View):
    """文章列表视图"""
    template_name = 'appblog/list.html'

    def get_context(self, category_id, tag_id):
        category = None
        tag = None
        if tag_id:
            article_list, tag = Article.get_by_tag(tag_id)
        elif category_id:
            article_list, category = Article.get_by_category(category_id)
        else:
            article_list = Article.latest_articles()

        context = {
            'category': category,
            'tag': tag,
            'article_list': article_list,
            'sidebars': SideBar.get_all(),
        }
        context.update(Category.get_navs())
        # print(context['navs'])
        # print(context['categories'])
        return context

    def get(self, request, category_id=None, tag_id=None):
        context = self.get_context(category_id, tag_id)
        return render(request, self.template_name, context=context)

    def post(self, request):
        pass


class ArticleDetailView(View):
    """文章细节视图"""
    template_name = 'appblog/detail.html'

    def get_context(self, article_id):
        try:
            # 通过get返回一条具体的class对象, 不是Queryset对象
            article = Article.get_all().get(id=article_id)
        except Article.DoesNotExist:
            article = None

        context = {
            'sidebars': SideBar.get_all(),
            'article': article,
        }
        context.update(Category.get_navs())
        return context

    def get(self, request, article_id=None):
        context = self.get_context(article_id)
        return render(request, self.template_name, context=context)

    def post(self, request):
        pass


class LinksView(View):
    """友链视图"""
    template_name = ''

    def get_context(self):
        context = {

        }
        return context

    def get(self):
        return HttpResponse('links')

    def post(self):
        pass


