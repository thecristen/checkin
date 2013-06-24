from django.conf.urls import patterns, url

from leaderboard import views

urlpatterns = patterns('',
    url(r'^$', views.topfivebv, name='index'),
    url(r'^topfivebv/$', views.topfivebv, name='topfivebv')
)
