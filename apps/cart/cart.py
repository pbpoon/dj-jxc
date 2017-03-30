from decimal import Decimal
from django.conf import settings
from product.models import Product,SlabList,SlabListItem


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart


    def add(self,slablist,slablistitem):
        product = Product.objects.get(slablist=slablist)
        product_id = str(product.id)
        slablist_id = str(slablist.id)
        type = product.type
        count = len(self.cart)
        if self.cart:
            for i in self.cart.values():
                if slablist_id in i.values():
                    i['slablistitem'] = slablistitem
                    i['thick'] = str(slablist.thick)
        else:
            count += 1
            self.cart[count] = {
                'product': product_id,
                'slablist': slablist_id,
                'slablistitem': slablistitem,
                'type': type,
                'key':count
            }
        self.save()
        print(self.cart)


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        # 用modified属性设定为True的方法来修改session
        self.session.modified = True

# # 把product在cart删除
    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = [i['product'] for i in self.cart.values()]
        # slablist_ls = [int(i['slablist']) for i in self.cart]
        products = Product.objects.filter(id__in = product_ids)
        # slablists = SlabList.objects.filter(pk__in =slablist_ls)
        # for product in products:
        #         self.cart['product']=product
        #     # self.cart[str(product.id)]['product'] = product
        #         print(self.cart)
        for item in self.cart.values():
            product_id = item['product']
            product = Product.objects.get(id =product_id)
            item['product'] = product
            if item['slablist']:
                slablist_id = item['slablist']
                slablist = SlabList.objects.get(id = slablist_id)
                item['slablist'] = slablist
            yield item
    #
    # def __len__(self):
    #     return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True