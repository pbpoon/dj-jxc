from django.contrib import admin
from .models import Supply,Contact,ImportOrder,ImportOrderDetail

class OrderItemInline(admin.TabularInline):
    model = ImportOrderDetail
    raw_id_fields = ['order']


@admin.register(ImportOrder)
class SlabListAdmin(admin.ModelAdmin):
    list_display = ['order', 'company', 'container', 'price', 'ps', 'updated', 'push_state', 'created', 'entry_user']
    list_filter = ['company', 'created', 'updated']
    inlines = [OrderItemInline]


class SupplyInline(admin.TabularInline):
    model = Contact
    raw_id_fields = ['company']


@admin.register(Supply)
class SlabListAdmin(admin.ModelAdmin):
    list_display = ['company', 'type', 'address', 'last_date', 'created',]
    list_filter = ['company', 'type', 'address']
    inlines = [SupplyInline]
