# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/3/22 9:21'

from django import forms
from .models import Category,Batch,Quarry

class BatchAddForm(forms.ModelForm):
    class Meta:
        model = Batch
        exclude = ['created']

