"""mingmingzhidao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'zhidao.views.index'),
    url(r'^index$','zhidao.views.index'),
    url(r'^search/(?P<key>[0-9]*)$', 'zhidao.views.pre_search'),
    url(r'^search/(?P<wd>(.+))/(?P<key>[0-9]*)$', 'zhidao.views.search'), 
    url(r'^login$', 'zhidao.views.login'),
    url(r'^register$','zhidao.views.register'),
    url(r'^logout$','zhidao.views.logout'),
    url(r'^information$','zhidao.views.usercenter'),
    url(r'^changepwd$','zhidao.views.changepwd'),
    url(r'^inforupdate$','zhidao.views.inforupdate'),
    url(r'^putquestion$','zhidao.views.putquestion'),
    url(r'^(?P<questionID>(.+))/(?P<userID>[0-9]*)/detail$','zhidao.views.questiondetail'),
    url(r'^(?P<questionID>(.+))/putanswer$','zhidao.views.putanswer')
    
]
