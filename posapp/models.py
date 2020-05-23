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
      
class ProductCategory(models.Model):
    cat_name        = models.CharField(max_length=150, unique=True)
    added_date      = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.cat_name
      
class ProductBrand(models.Model):
    brand_name      = models.CharField(max_length=150, unique=True)
    added_date      = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name
      
class ProductInfo(models.Model):
    product_cat     = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_brand   = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    product_name    = models.CharField(max_length=200, unique=True)
    added_date      = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
      
class PurchaseInfo(models.Model):
    purchase_invo   = models.IntegerField(default=0)
    product_cat     = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_brand   = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    product_name    = models.ForeignKey(ProductInfo, on_delete=models.CASCADE) 
    quantity        = models.IntegerField(default=0)
    unit_price      = models.FloatField(default=0)
    sales_price     = models.FloatField(default=0)
    purchase_date   = models.DateTimeField(auto_now_add=False)
    added_by        = models.ForeignKey(UserList, on_delete=models.CASCADE)
    added_date      = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product_name)
      
class SalesInfo(models.Model):
    sales_invo      = models.IntegerField(default=0)
    product_cat     = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_brand   = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    product_name    = models.ForeignKey(ProductInfo, on_delete=models.CASCADE) 
    quantity        = models.IntegerField(default=0)
    unit_price      = models.FloatField(default=0)  
    total_vat       = models.FloatField(default=0)  
    sales_by        = models.ForeignKey(UserList, on_delete=models.CASCADE)
    sales_date      = models.DateTimeField(auto_now_add=True)
    status          = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product_name)
      
class ProductInventory(models.Model):
    product_cat      = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_brand    = models.ForeignKey(ProductBrand, on_delete=models.CASCADE)
    product_name     = models.ForeignKey(ProductInfo, on_delete=models.CASCADE) 
    total_quantity   = models.IntegerField(default=0)
    current_quantity = models.IntegerField(default=0)   
    status           = models.BooleanField(default=True)

    def __str__(self):
        return str(self.current_quantity)
    
      
class DiscountInfo(models.Model):
    country_name     = models.ForeignKey(CountryList, on_delete=models.CASCADE)  
    from_month       = models.DateTimeField(auto_now_add=False)
    to_month         = models.DateTimeField(auto_now_add=False)
    from_amount      = models.IntegerField(default=0)   
    to_amount        = models.IntegerField(default=0)   
    discount         = models.IntegerField(default=0)   
    status           = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount)
    
