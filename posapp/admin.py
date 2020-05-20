from django.contrib import admin
from posapp import models

# Register your models here.


admin.site.register(models.CountryList)
admin.site.register(models.YearList)
admin.site.register(models.CompanySetup)
admin.site.register(models.UserList)