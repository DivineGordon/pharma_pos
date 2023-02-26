from django.contrib import admin

# Register your models here.

from .models import Product,DrugType,Supplier,StockedItem,StockEntry,SoldItem
# Register your models here.
admin.site.register(Product)
admin.site.register(DrugType)
admin.site.register(Supplier)
admin.site.register(StockedItem)
admin.site.register(StockEntry)
admin.site.register(SoldItem)
