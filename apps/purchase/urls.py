# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/3/22 16:23'
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add/$', views.addorder,name='addorder'),
    url(r'^(?P<order>\w+)/$', views.orderdetail,name='detail'),
    url(r'^', views.OrderListView.as_view(),name='index'),
        ]