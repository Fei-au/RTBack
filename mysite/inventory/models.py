import datetime
from django.db import models
from django.utils  import timezone
# Create your models here.


class Item_Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name + ': ' + description

class Supplier(models.Model):
    name = models.CharField(max_length=45)
    email = models.CharField(max_length=128, blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    added_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name + ': ' + address

class Item_Status(models.Model):
    status = models.CharField(max_length=40)
    def __str__(self):
        return self.status

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    bo_code = models.CharField(max_length=45, blank=True, null=True)
    number_code = models.CharField(max_length=45, blank=True, null=True)
    x_code = models.CharField(max_length=45, blank=True, null=True)
    lpn_code = models.CharField(max_length=45, blank=True, null=True)
    log_number = models.CharField(max_length=45, blank=True, null=True)
    msrp_price = models.DecimalField(max_digits=10,decimal_places=2)
    bid_start_price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Item_Category, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Item_Status, on_delete=models.CASCADE, blank=True, null=True)
    status_note = models.TextField(blank=True, null=True)
    quantity = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)
    add_date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.title + ': ' + self.description

    def was_added_recently(self):
        now = timezone.now()

        return now - datetime.timedelta(days=1) <= self.add_date <= now