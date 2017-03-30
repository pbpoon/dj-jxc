# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/3/16 23:55'
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<id>\d+)/$', views.product_detail,name='product_detail'),
    url(r'^slablist/(?P<id>\d+)/$', views.slablist_detail,name='slablist'),
    url(r'^', views.product_list,name='product_list'),
        ]