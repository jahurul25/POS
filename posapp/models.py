from django.db import models

# Create your models here.


class CountryList(models.Model):
    country_name  = models.CharField(max_length=30, unique=True)
    country_code  = models.CharField(max_length=10)
    added_date    = models.DateTimeField(auto_now_add=True)
    status        = models.BooleanField(default=True)

    def __str__(self):
        return self.country_name
    
class YearList(models.Model):
    year         = models.IntegerField(default=0)
    added_date   = models.DateTimeField(auto_now_add=True)
    status       = models.BooleanField(default=True)

    def __str__(self):
        return str(self.year)
      
class CompanySetup(models.Model):
    starting_year   = models.ForeignKey(YearList, on_delete=models.CASCADE)
    country_name    = models.ForeignKey(CountryList, on_delete=models.CASCADE)
    company_name    = models.CharField(max_length=200, unique=True)
    company_mobile  = models.CharField(max_length=15)
    company_email   = models.CharField(max_length=15)
    company_address = models.CharField(max_length=10)
    added_date      = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name
    
      
class UserList(models.Model):
    year            = models.ForeignKey(YearList, on_delete=models.CASCADE)
    country_name    = models.ForeignKey(CountryList, on_delete=models.CASCADE)
    company_name    = models.ForeignKey(CompanySetup, on_delete=models.CASCADE)
    user_full_name  = models.CharField(max_length=40)
    user_pass       = models.CharField(max_length=200)
    user_mobile     = models.CharField(max_length=15)
    user_email      = models.CharField(max_length=120, unique=True)
    user_address    = models.CharField(max_length=10)
    added_date      = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.user_full_name
    
