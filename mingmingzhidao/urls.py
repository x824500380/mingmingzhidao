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

urlpatterns = [
    url(r'^$', 'zhidao.views.index'),
    url(r'^index$','zhidao.views.index'),
    url(r'^search/(?P<key>[0-9]*)$', 'zhidao.views.pre_search'),
    url(r'^search/(?P<wd>(.+))/(?P<key>[0-9]*)$', 'zhidao.views.search'), 
    url(r'^login$', 'zhidao.views.login'),
    url(r'^register$','zhidao.views.register'),
    url(r'^logout$','zhidao.views.logout'),
    url(r'^usercenter/information$','zhidao.views.usercenter'),
    url(r'^usercenter/changepwd$','zhidao.views.changepwd'),
    url(r'^usercenter/inforupdate$','zhidao.views.inforupdate'),
    url(r'^putquestion$','zhidao.views.putquestion'),
    url(r'^(?P<questionID>(.+))/(?P<userID>[0-9]*)/detail$','zhidao.views.questiondetail'),
    url(r'^(?P<questionID>(.+))/putanswer$','zhidao.views.putanswer'),
    url(r'^usercenter/myquestions$','zhidao.views.myquestions'),
    url(r'^usercenter/myanswers$','zhidao.views.myanswers'),
    url(r'^(?P<answerID>(.+))/isbestanswer$','zhidao.views.isbestanswer'),
    url(r'^message/list$','zhidao.views.messagelist'),
    url(r'^(?P<messageID>(.+))/viewmessage$','zhidao.views.viewmessage'),
    url(r'^(?P<messageID>(.+))/setmessage$','zhidao.views.setmessage'),
    url(r'^(?P<messageID>(.+))/delete/message$','zhidao.views.deletemessage'),
    url(r'^set/allmessage$','zhidao.views.setallmessage'),
    url(r'^delete/allmessage$','zhidao.views.deleteallmessage'),
    url(r'^usercenter/timetree$','zhidao.views.timetree'),
    url(r'^(?P<answerID>(.+))/exquestion$','zhidao.views.exquestion')
]
