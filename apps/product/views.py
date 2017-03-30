from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,SlabListItem,SlabList,Category


def product_list(request,category=None):
    category = None
    products = Product.objects.all()
    # if category:
    #     category = Category.objects.get(category = category)
    #     products = Product.objects.filter(category = category)
    return render(request, 'product/list.html', locals())


def product_detail(request,id):
    product = get_object_or_404(Product,id=id)
    slablist = SlabList.objects.filter(block_num=product)
    return render(request, 'product/detail.html', locals())


def slablist_detail(request,id):
    slablist = get_object_or_404(SlabList, id=id)
    slablistitem = SlabListItem.objects.filter(slablistitem=slablist)
    if request.method =='POST':
        chk = request.POST.getlist('check_box_list')

        return
    return render(request, 'product/slablist.html', locals())
