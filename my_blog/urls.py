"""my_blog URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from articles import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name="home"),
    url(r'^(?P<page>\d*)$', views.home, name='paging_home'),
    url(r'^signin/$', views.sign_in, name='sign_in'),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^articles/', include("articles.urls")),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^archives/(?P<page>\d+)$', views.archives, name='paging_archives'),
    url(r'^tag/(?P<tag>\w+)/$', views.search_tag, name='search_tag'),
    url(r'^time/(?P<time>\S+)/$', views.search_time, name='search_time'),
    url(r'^aboutme/$', views.about_me, name='about_me'),
    url(r'^search/$', views.blog_search, name='search'),
    url(r'^write/$', views.write_blog, name='write'),
    url(r'^author/(?P<username>\w+)/$', views.personal_page, name='personal_page'),
    url(r'^delete/$', views.delete_article, name='delete_art'),
    url(r'^update/$', views.update_article, name='update_art'),
]
