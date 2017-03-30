from django.db import models

# Create your models here.
class CartItem(models.Model):
    product = models.ForeignKey('product.Product')
    slablist = models.ForeignKey('product.SlabList')
    total_price = models.DecimalField(max_digits=9, decimal_places=2)