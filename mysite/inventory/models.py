import datetime
from django.db import models
from django.utils  import timezone
import os
import logging

# Create your models here.


def upload_to(instance, filename):
    # Format the current date as YYYYMMDD
    date_prefix = datetime.datetime.now().strftime('%Y%m%d')
    # Return the path with the date prefix and the original filename
    return f'image/{date_prefix}/{filename}'
class Item_Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50)
    parent_size = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,related_name='children')
    category = models.ForeignKey(Item_Category,on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name + ': ' + self.description
class Color(models.Model):
    name = models.CharField(max_length=50)
    parent_color = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='children')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name + ': ' + self.description

class Supplier(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    added_date = models.DateField(default=datetime.date.today)
    def __str__(self):
        return self.name + ': ' + address

class Item_Status(models.Model):
    status = models.CharField(max_length=40)
    def __str__(self):
        return self.status


class Item(models.Model):
    class StockStatus(models.TextChoices):
        IN_STOCK = "In stock", "In stock",
        SOLD = "Sold", "Sold",
        RETURNED = "Returned", "Returned",
    case_number = models.CharField(max_length=12, default=1)
    item_number = models.CharField(max_length=20, default=1, blank=True, null=True)
    version = models.CharField(max_length=4, default='A') # The version of item number, eg: 1, 2, 3...
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    b_code = models.CharField(max_length=45, blank=True, null=True)
    upc_code = models.CharField(max_length=45, blank=True, null=True)
    ean_code = models.CharField(max_length=45, blank=True, null=True)
    fnsku_code = models.CharField(max_length=45, blank=True, null=True)
    lpn_code = models.CharField(max_length=45, blank=True, null=True)
    msrp_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    bid_start_price = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    category = models.ForeignKey(Item_Category, on_delete=models.SET_NULL, blank=True, null=True)
    standard_size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    customize_size = models.CharField(max_length=30, blank=True, null=True)
    standard_color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    customize_color = models.CharField(max_length=30, blank=True, null=True)
    status = models.ForeignKey(Item_Status, on_delete=models.DO_NOTHING, blank=True, null=True)
    status_note = models.TextField(blank=True, null=True)# Status note for not new items
    last_modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    add_date = models.DateTimeField(auto_now_add=True, blank=True, null=True) # First add date
    add_staff = models.ForeignKey('staff.Profile', on_delete=models.DO_NOTHING, blank=True, null=True) # Staff who add the item
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    stock_status = models.CharField(max_length=20, choices=StockStatus.choices,default=StockStatus.IN_STOCK,blank=True,null=True)
    shelf = models.IntegerField(blank=True,null=True) # Shelf number of item location, eg: 1, 2, 3...
    layer = models.CharField(max_length=1, blank=True,null=True) # Shelf layer of item location, eg: A, B, C...
    def __str__(self):
        return self.title + ': ' + self.description

    def was_added_recently(self):
        now = timezone.now()

        return now - datetime.timedelta(days=1) <= self.add_date <= now


class Image(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    local_image = models.ImageField(upload_to=upload_to, blank=True, null=True);
    external_url = models.URLField(max_length=255, blank=True, null=True);

    # def __str__(self):
    #     return f"Image for {self.item.title}"
    def delete(self, *args, **kwargs):
        if self.local_image:
            if os.path.isfile(self.local_image.path):
                os.remove(self.local_image.path)
        super().delete(*args, **kwargs)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "Pending", "Pending"
        PROCESSING = "Processing", "Processing"
        # For delivery
        SHIPPED = "Shipped", "Shipped"
        DELIVERED= "Delivered", "Delivered"
        # For pickup in store
        READY_FOR_PICKUP = "Ready for pickup", "Ready for pickup"
        SIGNED = "Signed", "Signed"
        # Cancelled or payment failed
        CANCELLED = "Cancelled" , "Cancelled"
        FAILED = "Failed", "Failed"

    # Post purchase actions put into another action table
#         RETURNED = "Returned",  "Returned" # Return whole order
#         PARTIALLY_RETURNED = "Partially returned","Partially returned"
#         EXCHANGE_REQUESTED = "Exchange requested", "Exchange requested"
#         REFUNED = "Refund", "Refund"
#     Payment Adjusted


    # class PaymentStatus(models.TextChoices):
    # pending
    # COMPLETED
    # FAILED

    invoice_number = models.IntegerField()
    # customer_id = models.ForeignKey()
    order_date = models.DateTimeField(default=datetime.datetime.now)
    total_amunt = models.DecimalField(max_digits=10,decimal_places=2)
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    # payment_status = models.ForeignKey(Payment)
class Shipping(models.Model):
    class ShippingMethod(models.TextChoices):
        UPS = "UPS", "UPS"
        CANADAPOST = "Canada Post", "Canada Post"
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    shipping_address = models.CharField(max_length=255)
    shipping_method = models.CharField(max_length=30,choices=ShippingMethod.choices,blank=True,null=True)
    tracking_number = models.CharField(max_length=50,blank=True,null=True)
    shipping_date = models.DateField(blank=True,null=True)
    delivery_date = models.DateField(blank=True,null=True)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=3,decimal_places=2,blank=True,null=True)
    note=models.CharField(max_length=200, blank=True,null=True)


