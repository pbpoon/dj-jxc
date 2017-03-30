# _*_ coding:utf-8 _*_
__author__ = 'pb'
__date__ = '2017/3/16 23:55'
from django.db import models

BLOCK_TYPE_CHOICES=(('block', '荒料'),('coarse', '毛板'),('slab', '板材'))

class Product(models.Model):
    block_num = models.CharField(max_length=20, unique=True, null=False, db_index= True, verbose_name=u'编号')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name=u'重量')
    long = models.IntegerField(null=True, verbose_name=u'长')
    width = models.IntegerField(null=True, verbose_name=u'宽')
    high = models.IntegerField(null=True, verbose_name=u'高')
    m3 = models.DecimalField(null=True, max_digits=5, decimal_places=2, verbose_name=u'立方')
    batch = models.ForeignKey('Batch', null=False, on_delete=models.CASCADE, verbose_name=u'批次')
    # store = models.ForeignKey('Store',null=True,bl,on_delete=models.SET_NULL,verbose_name=u'库存地址')
    type = models.CharField(max_length=6,choices=BLOCK_TYPE_CHOICES,null=False, verbose_name=u'形态')
    import_order = models.ForeignKey('purchase.ImportOrder',null=True,blank=True, verbose_name=u'进口代理单')
    updated = models.DateTimeField(auto_now=True, verbose_name=u'更新日期')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加日期')
    ccl_state = models.BooleanField(default=True,verbose_name=u'出材率计算方式')
    class Meta:
        verbose_name = u'产品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.block_num

    # def get_ccl(self):
    #     if self.type == 'slab':
    #         if self.ccl_state:
    #             return int(self.slablist.get_total_m2)/self.weight
    #         return int(self.slablist.get_total_m2)/self.m3
    #     return


class SlabList(models.Model):
    block_num = models.ForeignKey('Product',related_name='slablist',on_delete=models.CASCADE, verbose_name=u'荒料编号')
    user = models.CharField(max_length=20, null=False, verbose_name=u'录入人员')#日后更改外键user表
    ps = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'备注信息')
    thick = models.DecimalField(max_digits=4, decimal_places=2, null=False, verbose_name=u'厚度')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加日期')
    updated = models.DateTimeField(auto_now=True, verbose_name=u'更新日期')

    class Meta:
        verbose_name = u'码单信息'
        verbose_name_plural = verbose_name


class SlabListItem(models.Model):
    slablistitem = models.ForeignKey('SlabList',related_name='items', verbose_name=u'码单')
    part_num = models.CharField(max_length=8, verbose_name=u'夹号')
    part_index = models.PositiveSmallIntegerField(u'序号')
    long = models.PositiveSmallIntegerField(verbose_name=u'长')
    high = models.PositiveSmallIntegerField(verbose_name=u'高')
    kl1 = models.PositiveSmallIntegerField(null=True,blank=True, verbose_name=u'长1')
    kl2 = models.PositiveSmallIntegerField(null=True,blank=True, verbose_name=u'长2')
    kh1 = models.PositiveSmallIntegerField(null=True,blank=True, verbose_name=u'高1')
    kh2 = models.PositiveSmallIntegerField(null=True,blank=True, verbose_name=u'高2')
    m2 = models.DecimalField(max_digits=5,decimal_places=2,verbose_name=u'平方')
    is_sell = models.BooleanField(default=False, verbose_name=u'是否已售')
    is_booking = models.BooleanField(default=False, verbose_name=u'是否已定')
    is_pickup = models.BooleanField(default=False, verbose_name=u'是否已提货')


    def save(self,*args,**kwargs):
        self.m2 = (self.long * self.high)/10000-(self.kl1 * self.kh1)/10000-(self.kl2 * self.kh2)/10000
        print(self.m2)
        super(SlabListItem, self).save(*args, **kwargs)

    # def get_m2(self):
    #      m2 = self.long(self.long * self.high)*0.0001-(self.kl1 * self.kh1)*0.0001-(self.kl2 * self.kh2)*0.0001
    #     return slablistitem.pk


class Batch(models.Model):
    name = models.CharField(max_length=20, unique=True, db_index=True, verbose_name=u'批次编号')
    category = models.ForeignKey('Category', verbose_name=u'品种名称')
    quarry = models.ForeignKey('Quarry', null=False, verbose_name=u'矿口')
    # supply = models.ForeignKey('Supply', null=False, verbose_name=u'贸易公司')
    buy_price = models.PositiveIntegerField(null=True,blank=True, verbose_name=u'采购价格')
    buy_date = models.DateField(null=True,blank=True, verbose_name=u'采购日期')
    ps = models.CharField(max_length=200,null=True,blank=True, verbose_name=u'备注信息')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加日期')

    class Meta:
        verbose_name = u'批次信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}票'.format(self.name)


class Category(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True, db_index=True, verbose_name=u'品种名称')
    created = models.DateField(auto_now_add=True, verbose_name=u'添加日期')

    class Meta:
        verbose_name = u'品种信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Quarry(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True, verbose_name=u'矿口名称')
    desc = models.CharField(max_length=200,verbose_name=u'描述信息')
    created = models.DateField(auto_now_add=True, verbose_name=u'添加日期')
    updated = models.DateField(auto_now=True, verbose_name=u'更新日期')

    class Meta:
        verbose_name = u'矿口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Store(models.Model):
    pass