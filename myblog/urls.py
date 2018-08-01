"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from blog.views import *
from blog.feeds import BlogRssFeed


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^archive/$', archive, name='archive'),
    url(r'^tags/$', tags, name='tags'),
    url(r'^tags/(?P<tag_name>\w+)$', tag_detail, name='tag_name'),
    url(r'^blog/(?P<blog_id>\d+)$', blog_detail, name='blog_id'),
    url(r'^add_comment/$', add_comment, name='add_comment'),
    url(r'^rss/$', BlogRssFeed(), name='rss'),
    url(r'^category/(?P<category_name>\w+)/$', category_detail, name='category_name'),
]
