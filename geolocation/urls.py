# -*-coding:utf-8-*-
from django.urls import re_path
from geolocation import views

urlpatterns = [
    re_path(r'^user_access_charts/$', views.user_access_charts, name='user_access_charts'),
    re_path(r'^geolocation_charts/$', views.geolocation_charts, name='geolocation_charts'),
    re_path(r'^path_access_charts/$', views.path_access_charts, name='path_access_charts'),

]
