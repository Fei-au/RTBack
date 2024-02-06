from django.contrib import admin
from .models import Item, Item_Status, Item_Category, Supplier
# Register your models here.

# class ItemAdmin(admin.ModelAdmin):
#     fields = ["description", "title"]

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Date information", {"fields": ["description"]}),
    ]
admin.site.register(Item, ItemAdmin)
admin.site.register(Item_Status)
admin.site.register(Item_Category)
admin.site.register(Supplier)

