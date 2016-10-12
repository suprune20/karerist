# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', views.ulogin, name='ulogin'),
    url(r'^logout/$', views.ulogout, name='ulogout'),
]
