# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/3/22 12:25'

from django import forms
from .models import ImportOrder,ImportOrderDetail
from product.models import Product


class ImportOrderForms(forms.ModelForm):
    class Meta:
        model = ImportOrder
        exclude = ['created']
        widgets = {
            'order':forms.HiddenInput()
        }


# ImportOrderDetailFormset = inlineformset_factory(ImportOrder, ImportOrderDetail, exclude=('order',))

class ImportProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['type', 'updated', 'created']
        widgets ={
            'block_num':forms.TextInput(attrs={
                'size':'5'
            }),
            'weight': forms.TextInput(attrs={
                'size': '5'
            }),
            'long': forms.TextInput(attrs={
                'size': '5'
            }),
            'width': forms.TextInput(attrs={
                'size': '5'
            }),
            'high':forms.TextInput(attrs={
                'size':'5'
            }),
            'm3': forms.TextInput(attrs={
                'size': '5'
            }),

        }


# ImportOrderDetailFormset = inlineformset_factory(ImportOrder, form=ImportProductForm)


class ExcelFileForm(forms.Form):
    excelfile = forms.FileField()