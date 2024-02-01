from django.contrib import admin
from .models import Item, Item_Status, Item_Category, Supplier
# Register your models here.

admin.site.register(Item)
admin.site.register(Item_Status)
admin.site.register(Item_Category)
admin.site.register(Supplier)

