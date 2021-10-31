# -*-coding:utf-8-*-
from django.urls import path,include,re_path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('user_access', views.user_access_charts, name='user_access'),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.articles, name='articles'),
]
