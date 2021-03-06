from django.contrib import admin
from posapp import models

# Register your models here.


admin.site.register(models.CountryList)
admin.site.register(models.YearList)
admin.site.register(models.CompanySetup)
admin.site.register(models.UserList)
admin.site.register(models.PurchaseInfo)
admin.site.register(models.SalesInfo)
admin.site.register(models.ProductInventory)
admin.site.register(models.DiscountInfo)
admin.site.register(models.GiftCard)
admin.site.register(models.InvoiceWiseDiscount)
admin.site.register(models.SalesPaymentInfo)