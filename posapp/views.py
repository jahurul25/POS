from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.utils import timezone
from posapp import models
from django.http import JsonResponse
from django.contrib import messages
import json, hashlib

# Create your views here.

def user_login(request):
    # try:
        if request.method == "GET":
            return render(request, "posapp/common/user_login.html")
        else:
            user_email = request.POST["user_email"].strip()
            user_pass  = request.POST["user_pass"].strip()
             
            encrypt_pass   = hashlib.md5(user_pass.encode()).hexdigest()
            print("encrypt_pass: ", encrypt_pass)
            chk_user_login = models.UserList.objects.filter(user_email=user_email, user_pass=encrypt_pass, status=True).first()
            if chk_user_login:
                request.session["userid"] = chk_user_login.pk
                request.session["companyid"] = chk_user_login.company_name_id
                request.session["user_full_name"] = chk_user_login.user_full_name
                return redirect("/dashboard/")
            else:
                return render(request, "posapp/common/user_login.html")
    # except:
    #     return redirect("/login/")  

def user_logout(request):
    request.session["userid"] = None
    request.session["companyid"] = None
    request.session["user_full_name"] = None
    return redirect("/login/")
    

def dashboard(request):
    if request.session["userid"]:
        dt = models.CountryList.objects.all() 
        return render(request, "posapp/common/dashboard.html")
    else:
        return redirect("user_logout")
         

def user_profile(request):
    if request.session["userid"]:
        context = {"user": models.UserList.objects.filter(pk = request.session["userid"]).first() }
        return render(request, "posapp/common/user_profile.html", context)
    else:
        return redirect("user_logout")
    
def user_list(request):
    if request.session["userid"]:
        context = { "user_list": models.UserList.objects.all() }
        return render(request, "posapp/settings/user_list.html", context)
    else:
        return redirect("user_logout")
    
def user_registration(request):
    if request.session["userid"]:
        if request.method == "GET":
            context = {
                "country_list": models.CountryList.objects.filter(status=True),
                "year_list": models.YearList.objects.filter(status=True) 
            }
            return render(request, "posapp/common/user_registration.html", context)
        elif request.method == "POST":
            year_name      = int(request.POST["year_name"])
            country_name   = int(request.POST["country_name"])
            user_full_name = request.POST["user_full_name"].strip()
            user_mobile    = request.POST["user_mobile"].strip()
            user_email     = request.POST["user_email"].strip()
            user_pass      = request.POST["user_pass"].strip()
            user_address   = request.POST["user_address"].strip()
            
            encrypt_pass   = hashlib.md5(user_pass.encode()).hexdigest()
            models.UserList.objects.create(
                year_id = year_name, country_name_id = country_name, user_full_name = user_full_name, company_name_id = request.session["companyid"],
                user_mobile = user_mobile, user_email = user_email, user_pass = encrypt_pass, user_address = user_address
            )
            messages.success(request, "User registraion successful")
            return redirect("user_list")
    else:
        return redirect("user_logout")    

def country_list(request): 
    if request.session["userid"]:
        if request.method == "GET": 
            context = { "country_list": models.CountryList.objects.all() }
            return render(request, "posapp/settings/country_list.html", context)
    else:
        return redirect("user_logout") 

def year_list(request): 
    if request.session["userid"]:
        context = { "year_list": models.YearList.objects.all() }
        return render(request, "posapp/settings/year_list.html", context)
    else:
        return redirect("user_logout") 
    
def company_setup(request): 
    if request.session["userid"]:
        context = { "company_info": models.CompanySetup.objects.all() }
        return render(request, "posapp/settings/company_setup.html", context)
    else:
        return redirect("user_logout") 

def add_product_category(request): 
    if request.session["userid"]:
        if request.method == "GET":
            return render(request, "posapp/settings/add_product_category.html")
        else:
            cat_name = request.POST["cat_name"].strip()
            models.ProductCategory.objects.create(cat_name = cat_name)
            messages.success(request, "Category add successful")
            return redirect("product_category_list")          
    else:
        return redirect("user_logout") 
    
def product_category_list(request): 
    if request.session["userid"]:
        context = { "cat_list": models.ProductCategory.objects.all() }
        return render(request, "posapp/settings/product_category_list.html", context)
    else:
        return redirect("user_logout") 
    
def add_product_brand(request): 
    if request.session["userid"]:
        if request.method == "GET":
            return render(request, "posapp/settings/add_product_brand.html")
        else:
            brand_name = request.POST["brand_name"].strip()
            models.ProductBrand.objects.create(brand_name = brand_name)
            messages.success(request, "Brand add successful")
            return redirect("product_brand_list") 
    else:
        return redirect("user_logout") 
    
def product_brand_list(request): 
    if request.session["userid"]:
        context = { "brand_list": models.ProductBrand.objects.all() }
        return render(request, "posapp/settings/product_brand_list.html", context)
    else:
        return redirect("user_logout") 
    
def add_product_name(request): 
    if request.session["userid"]:
        if request.method == "GET":
            context = {
                "cat_list": models.ProductCategory.objects.filter(status=True),
                "brand_list": models.ProductBrand.objects.filter(status=True)
            }
            return render(request, "posapp/settings/add_product_name.html", context)
        else:
            cat_name     = request.POST["cat_name"] 
            brand_name   = request.POST["brand_name"] 
            product_name = request.POST["product_name"].strip()
            models.ProductInfo.objects.create(product_cat_id = cat_name, product_brand_id = brand_name, product_name = product_name)
            messages.success(request, "Product name add successful")
            return redirect("product_name_list") 
    else:
        return redirect("user_logout") 
    
def product_name_list(request): 
    if request.session["userid"]:
        context = { "product_name_list": models.ProductInfo.objects.all() }
        return render(request, "posapp/settings/product_name_list.html", context)
    else:
        return redirect("user_logout") 
    
def purchase_entry(request):
    if request.session["userid"]: 
        if request.method == "GET":
            purchase_invo = models.PurchaseInfo.objects.order_by("-purchase_invo").first()
            if purchase_invo:
                purchase_invo += 1
            else:
                purchase_invo = 100001    
            
            print("timezone: ", timezone.now())
            context = {
                "current_date": timezone.now(),
                "purchase_invo": purchase_invo,
                "cat_list": models.ProductCategory.objects.filter(status=True),
                "brand_list": models.ProductBrand.objects.filter(status=True),
                "product_list": models.ProductInfo.objects.filter(status=True)
            }
            return render(request, "posapp/common/purchase_entry.html", context)
        else:
            return redirect("purchase_entry") 
    else:
        return redirect("user_logout") 
    
def sales_entry(request): 
    if request.session["userid"]: 
        return render(request, "posapp/common/sales_entry.html")
    else:
        return redirect("user_logout") 
    
def inventory(request): 
    if request.session["userid"]: 
        return render(request, "posapp/common/inventory.html")
    else:
        return redirect("user_logout") 
