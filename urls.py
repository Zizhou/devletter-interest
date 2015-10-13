from django.conf.urls import patterns, url

from interest import views

urlpatterns = patterns('',
    url(r'^poll/$', views.poll, name = 'poll'),
    url(r'^poll2/$', views.poll2, name = 'poll2'),
    url(r'^bulk/$', views.bulk, name = 'bulk'),
    url(r'^result/$', views.result, name = 'result'),
    url(r'^$', views.main_page, name = 'main'),
)
