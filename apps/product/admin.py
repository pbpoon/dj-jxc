from django.contrib import admin
from .models import Product,SlabList,SlabListItem,Batch,Category,Quarry
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


class SlabListItemInline(admin.TabularInline):
    model = SlabListItem
    raw_id_fields = ['slablistitem']


@admin.register(SlabList)
class SlabListAdmin(admin.ModelAdmin):
    list_display = ['block_num','user','ps','thick','created','updated']
    list_filter = ['thick','created','updated']
    inlines = [SlabListItemInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Quarry)
class QuarryAdmin(admin.ModelAdmin):
    pass

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    pass
