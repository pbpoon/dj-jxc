from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Supply, ImportOrder, ImportOrderDetail
from .forms import ImportProductForm, ExcelFileForm, ImportOrderForms
import xlrd
from decimal import *


class OrderListView(ListView):
    queryset = ImportOrder.objects.all()  # 日后现实发布状态为是的
    context_object_name = 'order_list'
    template_name = 'purchase/list.html'


def orderdetail(request, order):
    order = get_object_or_404(ImportOrder, order=order)
    orderitems = order.product_set.all()
    total = orderitems.aggregate(weight=sum('weight'))
    count = orderitems.count()
    return render(request, 'purchase/detail.html', locals())


def addorder(request):
    if request.method == 'POST':
        form = ImportOrderForms(request.POST, request.FILES)
        fileform = ExcelFileForm(request.POST, request.FILES)
        if fileform.is_valid() and form.is_valid():
            order = form.save(commit=False)
            form.save()
            from product.models import Product
            f = request.FILES.get('excelfile')
            if f:
                data = xlrd.open_workbook(file_contents=f.read())
                # table = data.sheet_by_name(by_name)
                table = data.sheets()[0]
                nrows = table.nrows  # 行数
                colnames = table.row_values(0)  # 表头列名称数据
                print(colnames)
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
                return redirect(order)
    else:
        form = ImportOrderForms()
        fileform = ExcelFileForm()
    return render(request, 'purchase/addorder.html', locals())
