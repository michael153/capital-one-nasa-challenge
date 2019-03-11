from django.conf.urls import url

from . import views

app_name = 'web'
urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^search_tags/$', views.search_tags_view, name='search_tags'),
    url(r'^fastsearch/$', views.fastsearch_view, name='fastsearch'),
    url(r'^search/$', views.search_view, name='search'),
]