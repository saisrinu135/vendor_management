from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import F
from django.db.models import Avg, Count

class Vendor(models.Model):
    vendor_code = models.CharField(unique = True, max_length = 50)
    name = models.CharField(max_length = 50, null = True, blank = True)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    
    @property
    def vendor_code(self):
        prefix = 'VENDOR'
        code = str(self.id).zfill(4)
        return prefix + code
    
    @vendor_code.setter
    def vendor_code(self, value):
        self.vendor_code = value
    
    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    po_number = models.CharField(unique = True, max_length = 50, primary_key = True)              
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE, related_name = "purchase_orders")
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null = True, blank = True)
    delivered_date = models.DateTimeField(null = True, blank = True)
    items = models.JSONField()    
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length = 20, choices = (("pending", "Pending"), ("completed", "Completed"), ("canceled", "Canceled")))
    quality_rating = models.FloatField(null = True, blank = True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null = True, blank = True)
    
    def __str__(self):
        return self.po_number



class Performance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE, related_name = "vendor_performance")
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField(null = True, blank = True)
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


@receiver(post_save, sender = PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.delivered_date is None:
        instance.delivered_date = timezone.now()
        instance.save()
        
    # Update on time delivery
    completed_orders = PurchaseOrder.objects.filter(status = 'completed', vendor = instance.vendor)
    on_time_deliveries = completed_orders.filter(delivered_date__lte = F("delivery_date"))
    
    on_time_delivery_rate = on_time_deliveries.count() / completed_orders.count()
    
    instance.vendor.on_time_delivery_rate = on_time_delivery_rate if on_time_delivery_rate else 0
    
    # Update quality rating
    completed_orders_with_ratings = completed_orders.filter(quality_rating = True)
    quality_rating_avg = completed_orders_with_ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    instance.vendor.quality_rating_avg = quality_rating_avg if quality_rating_avg else 0
    instance.vendor.save()
    
@receiver(post_save, sender=PurchaseOrder)
def update_response_time(sender, instance, **kwargs):
    response_times = PurchaseOrder.objects.filter(vendor = instance.vendor, acknowledgement_date__isnull = False).values_list('acknowledgement_data', 'issue_date')
    response_time_avg = response_times.aggregate(Avg('acknowledgement_date') - Avg('issue_date'))['acknowledgement_date__avg'] or 0
    instance.vendor.average_response_time = response_time_avg if response_time_avg > 0 else 0
    instance.vendor.save()


@receiver(post_save, sender = PurchaseOrder)
def update_fulfillment_rate(sender, instance, **kwargs):
    fulfilment_orders = PurchaseOrder.objects.filter(vendor = instance.vendor, status = 'completed', quality_rating= True)
    fulfillment_rate = fulfilment_orders.count() / PurchaseOrder.objects.filter(vendor = instance.vendor, status = 'completed').count()
    instance.vendor.fulfillment_rate = fulfillment_rate if fulfillment_rate else 0
    instance.vendor.save()
    