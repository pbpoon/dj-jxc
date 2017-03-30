from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from product.models import Product,SlabList,SlabListItem
from .cart import Cart


@require_POST
def cart_add(request,slablist_id):
    cart = Cart(request)
    slablist = get_object_or_404(SlabList, id =slablist_id)
    chk = request.POST.getlist('check_box_list')
    cart.add(slablist =slablist, slablistitem = chk)
    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request,'cart/detail.html',locals())

def cart_slablist_detail(request,key):
    cart = Cart(request)
    slablistitem_ls = cart.cart[key]['slablistitem']
    slablist = get_object_or_404(SlabList, id=cart.cart[key]['slablist'])
    slablistitem = SlabListItem.objects.filter(id__in =slablistitem_ls)
    return render(request, 'product/slablist.html', locals())