# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/3/19 11:19'
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add/(?P<slablist_id>\d+)/$', views.cart_add,name='add'),
    url(r'^slablist/(?P<key>\d+)/$', views.cart_slablist_detail,name='slablist'),
    url(r'^$', views.cart_detail,name='detail'),
        ]

