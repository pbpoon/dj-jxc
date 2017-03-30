from django.db import models
from django.core.urlresolvers import reverse
import datetime


class Supply(models.Model):
    TYPE_CHOICES = (
        ('import', '进口代理'),
        ('quarry', '矿山'),
        ('trading', '贸易公司'),
    )
    company = models.CharField(max_length=50, null=False, unique=True, verbose_name=u'公司名称')
    type = models.CharField(choices=TYPE_CHOICES, max_length=18, null=False, verbose_name=u'类型')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name=u'地址')
    last_date = models.DateField(verbose_name=u'最后交易日期')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加日期')

    class Meta:
        verbose_name = u'供应商信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.company


class Contact(models.Model):
    name = models.CharField(max_length=20, null=False, verbose_name=u'名字')
    telephone = models.CharField(max_length=11, null=False, verbose_name=u'联系电话')
    telephone2 = models.CharField(max_length=11, null=False, verbose_name=u'联系电话2')
    email = models.EmailField(max_length=120, null=True, blank=True, verbose_name='邮件地址')
    company = models.ForeignKey('Supply', null=False, related_name='people',  on_delete=models.CASCADE,
                                verbose_name=u'所属公司')

    class Meta:
        verbose_name = u'供应商联系人信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ImportOrder(models.Model):
    # 日后需要改动order_ID的pk为日期格式
    order = models.CharField(max_length=12, default=u'a', null=True, blank=True, db_index=True, unique=True, verbose_name=u'订单号')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加日期')
    company = models.ForeignKey('Supply', related_name='im_order', null=False, on_delete=models.CASCADE,
                                verbose_name=u'代理公司')
    entry_user = models.ForeignKey('user.UserProfile', null=False, verbose_name=u'录入用户')
    container = models.SmallIntegerField(default=0, null=False, verbose_name=u'货柜数')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name=u'单价')
    ps = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'备注')
    push_state = models.BooleanField(default=False, verbose_name=u'发布状态')
    file = models.FileField(upload_to='purchase/%Y%m', blank=True,verbose_name=u'相关文件')
    updated = models.DateTimeField(auto_now=True, verbose_name=u'更新日期')

    class Meta:
        verbose_name = u'进口代理订单'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        # 格式为 IM1703001
        if self.order in ImportOrder.objects.values_list('order', flat=True):
            pass
        else:
            date_str = datetime.datetime.now().strftime('%y%m')
            last_record = ImportOrder.objects.last()
            # 判断是否为新表
            if last_record:
                last_id = last_record.order
                if date_str in last_id[2:6]:
                    self.order = 'IM' + str(int(last_id[2:9]) + 1)
                else:
                    self.order = 'IM' + date_str + '001' # 新月份
            else:
                self.order = 'IM' + date_str + '001' # 新记录
        super(ImportOrder, self).save(*args, **kwargs)

    def __str__(self):
        return self.order

    def get_absolute_url(self):
        return reverse('purchase:detail', args=[self.order])


class ImportOrderDetail(models.Model):
    order = models.ForeignKey('ImportOrder', related_name='order_items', null=False, on_delete=models.CASCADE,
                              verbose_name=u'订单号')
    block_num = models.ForeignKey('product.Product', null=False, on_delete=models.CASCADE, verbose_name=u'编号')

    class Meta:
        verbose_name = u'进口代理订单明细'
        verbose_name_plural = verbose_name
