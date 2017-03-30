from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,View
from .models import Supply,ImportOrder,ImportOrderDetail,Contact
from .forms import ImportOrderDetailFormset
from django.forms.models import modelformset_factory
from product.models import Product

class OrderListView(ListView):
    queryset = ImportOrder.objects.all()# 日后现实发布状态为是的
    context_object_name = 'order_list'
    template_name = 'purchase/list.html'


def orderdetail(request, order):
    order = get_object_or_404(ImportOrder, order = order)
    orderitems = ImportOrderDetail.objects.filter(order=order)
    itemlist ={}
    for item in orderitems:
        itemlist[str(item.block_num)] = {'block_num':item.block_num}
    return render(request,'purchase/detail.html', locals())


def addorder(request):
    if request.method == 'POST':
        formset = ImportOrderDetailFormset(request.POST, request.FILES)
        if formset.is_valid():
            pass
    else:
        formset = ImportOrderDetailFormset(auto_id=False)
    return render(request, 'purchase/addorder.html',locals())
