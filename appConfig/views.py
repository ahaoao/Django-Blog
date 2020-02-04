from django.views.generic import ListView
from appBlog.views import CommonViewMixin
from .models import Link


# Create your views here.
class LinkListView(CommonViewMixin, ListView):
    """友链视图"""
    queryset = Link.get_normal()
    template_name = 'appconfig/links.html'
    context_object_name = 'link_list'
