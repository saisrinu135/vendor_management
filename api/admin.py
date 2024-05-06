from django.contrib import admin
from .models import Vendor, PurchaseOrder, Performance

# Register your models here.



admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(Performance)

class VendorAdmin(admin.ModelAdmin):
    list_display = ('vendor_code', 'name', 'contact_details', 'address', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'status', 'order_date', 'delivery_date')

class PerfromanceAdmin(admin.ModelAdmin):
    list_display = ('vendor_no')