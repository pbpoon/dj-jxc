from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    setcor = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'部门')
    wechat = models.CharField(max_length=120, null=True, blank=True, verbose_name=u'微信号')
    gender = models.CharField(max_length=12, choices=(('male', '男'), ('female', '女')))
    telephone = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'联系电话')
    image = models.ImageField(upload_to='user/%Y%m', default='user/default.png', max_length=100, verbose_name=u'头像')

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()