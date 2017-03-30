from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView
from django.db.models import Avg, Sum
from .models import Supply, ImportOrder, ImportOrderDetail
from .forms import ImportProductForm, ExcelFileForm, ImportOrderForms
from django.forms.models import inlineformset_factory
from product.models import Product
import xlrd
from decimal import *


class OrderListView(ListView):
    queryset = ImportOrder.objects.all()  # 日后现实发布状态为是的
    context_object_name = 'order_list'
    template_name = 'purchase/list.html'


def orderdetail(request, order):
    order = get_object_or_404(ImportOrder, order=order)
    orderitems = order.product_set.all()
    total = orderitems.aggregate(weight=Sum('weight'))
    count = orderitems.count()
    return render(request, 'purchase/detail.html', locals())


def addorder(request):
    if request.method == 'POST':
        form = ImportOrderForms(request.POST, request.FILES)
        fileform = ExcelFileForm(request.POST, request.FILES)
        if fileform.is_valid() and form.is_valid():
            order = form.save(commit=False)
            from product.models import Product
            f = request.FILES.get('excelfile')
            if f:
                data = xlrd.open_workbook(file_contents=f.read())
                # table = data.sheet_by_name(by_name)
                table = data.sheets()[0]
                nrows = table.nrows  # 行数
                colnames = table.row_values(0)  # 表头列名称数据
                list = []
                for rownum in range(1, nrows):
                    row = table.row_values(rownum)
                    if row:
                        for i in range(len(colnames)):
                            if isinstance(row[i], float):
                                row[i] = Decimal(row[i])
                            else:
                                row[i] = str(row[i])
                    if not Product.objects.filter(block_num=row[0]):
                        list.append(Product(block_num=row[0], weight=row[5], long=row[1], width=row[2],
                                            high=row[3], m3=row[4], batch_id=1, import_order=order))
                Product.objects.bulk_create(list)
                form.save()
                return redirect(order)
    else:
        form = ImportOrderForms()
        fileform = ExcelFileForm()
    return render(request, 'purchase/addorder.html', locals())


def editorder(request,order):
    IPformset = inlineformset_factory(ImportOrder,Product,form=ImportProductForm)
    obj = get_object_or_404(ImportOrder, order=order)
    orderitems = obj.product_set.all()
    if request.method == 'POST':
        form = ImportOrderForms(request.POST, request.FILES)
        formset = IPformset(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            formset.save()
        return redirect(obj)
    form = ImportOrderForms(instance=obj)
    formset = IPformset(instance=obj)
    return render(request, 'purchase/edit.html',locals())