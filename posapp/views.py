from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.utils import timezone
from posapp import models
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import F
import json, hashlib, requests
from posapp.templatetags import custom_tags
from django.db.models import Count  

# Create your views here.

def user_login(request):
    try:
        if request.method == "GET":
            return render(request, "posapp/common/user_login.html")
        else:
            user_email = request.POST["user_email"].strip()
            user_pass  = request.POST["user_pass"].strip()
             
            encrypt_pass   = hashlib.md5(user_pass.encode()).hexdigest()

            chk_user_login = models.UserList.objects.filter(user_email=user_email, user_pass=encrypt_pass, status=True).first()
            if chk_user_login:
                request.session["userid"] = chk_user_login.pk
                request.session["companyid"] = chk_user_login.company_name_id
                request.session["user_country"] = chk_user_login.country_name.country_name
                request.session["user_full_name"] = chk_user_login.user_full_name
                return redirect("/dashboard/")
            else:
                return render(request, "posapp/common/user_login.html")
    except:
        return redirect("/login/")  

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
            invoice_number = 0
            get_invo = models.PurchaseInfo.objects.order_by("-purchase_invo").first()
            if get_invo:
                invoice_number += get_invo.purchase_invo + 1
            else:
                invoice_number = 100001    
             
            context = {
                "current_date": timezone.now(),
                "purchase_invo": invoice_number,
                "cat_list": models.ProductCategory.objects.filter(status=True),
                "brand_list": models.ProductBrand.objects.filter(status=True),
                "product_list": models.ProductInfo.objects.filter(status=True)
            }
            return render(request, "posapp/common/purchase_entry.html", context)
        else:
            return redirect("user_logout") 
    else:
        return redirect("user_logout") 
    
def purchase_list(request):
    if request.session["userid"]: 
        if request.method == "GET": 
            purchase_list = models.PurchaseInfo.objects.order_by("-purchase_invo")
            product_list  = models.ProductInfo.objects.filter(status=True)
            context = { 
                "purchase_list": purchase_list,
                "product_list": product_list,
            }
            return render(request, "posapp/common/purchase_list.html", context)
        else: 
            product_name  = int(request.POST["product_name"])
            purchase_list = models.PurchaseInfo.objects.filter(product_name_id = product_name).order_by("-purchase_invo")
            product_list  = models.ProductInfo.objects.filter(status=True)
            context = { 
                "product_name": product_name,
                "purchase_list": purchase_list,
                "product_list": product_list,
            }
            return render(request, "posapp/common/purchase_list.html", context)
    else:
        return redirect("user_logout") 
    
def sales_entry(request):  
    if request.session["userid"]: 
        if request.method == "GET":
            invoice_number = 0
            get_invo = models.SalesInfo.objects.order_by("-sales_invo").first()
            if get_invo:
                invoice_number += get_invo.sales_invo + 1
            else:
                invoice_number = 100001    
             
            vat  = 5
            if request.session["user_country"] == "USA":
                vat = 7
                 
            context = {
                "vat": vat,
                "current_date": timezone.now(),
                "sales_invo": invoice_number,
                "cat_list": models.ProductCategory.objects.filter(status=True),
                "brand_list": models.ProductBrand.objects.filter(status=True),
                "product_list": models.ProductInfo.objects.filter(status=True)
            } 
            return render(request, "posapp/common/sales_entry.html", context)
    else:
        return redirect("user_logout") 
    
def sales_list(request): 
    if request.session["userid"]: 
        if request.method == "GET": 
            sales_list = models.SalesInfo.objects.filter(sales_by_id = request.session["userid"], sales_complete=True).order_by("-sales_invo")
            product_list  = models.ProductInfo.objects.filter(status=True)
            context = { 
                "sales_list": sales_list,
                "product_list": product_list,
            }
            return render(request, "posapp/common/sales_list.html", context)
        else: 
            product_name  = int(request.POST["product_name"])
            sales_list = models.SalesInfo.objects.filter(sales_by_id = request.session["userid"], sales_complete=True, product_name_id = product_name).order_by("-sales_invo")
            product_list  = models.ProductInfo.objects.filter(status=True)
            context = { 
                "product_name": product_name,
                "sales_list": sales_list,
                "product_list": product_list,
            }
            return render(request, "posapp/common/sales_list.html", context)
    else:
        return redirect("user_logout") 
    
  
def sales_order_list(request): 
    if request.session["userid"]: 
        if request.method == "GET": 
            sales_list = models.SalesInfo.objects.filter(sales_by_id = request.session["userid"], sales_complete = False).order_by("-sales_invo")
             
            invoice_list  = models.SalesInfo.objects.values('sales_invo').annotate(dcount=Count('sales_invo')).filter(sales_by_id = request.session["userid"], sales_complete = False, status=True).order_by("-sales_invo")
            context = { 
                "sales_list": sales_list,
                "invoice_list": invoice_list,
            }
            return render(request, "posapp/common/sales_order_list.html", context)
        else: 
            sales_invo  = int(request.POST["sales_invo"])
            sales_list  = models.SalesInfo.objects.filter(sales_by_id = request.session["userid"], sales_invo = sales_invo, sales_complete = False).order_by("-sales_invo")
            invoice_list  = models.SalesInfo.objects.values('sales_invo').annotate(dcount=Count('sales_invo')).filter(sales_by_id = request.session["userid"], sales_complete = False, status=True).order_by("-sales_invo")
            context = { 
                "sales_invo": sales_invo,
                "sales_list": sales_list,
                "invoice_list": invoice_list,
            }
            return render(request, "posapp/common/sales_order_list.html", context)
    else:
        return redirect("user_logout") 
    
def discount_info(request): 
    if request.session["userid"]: 
        if request.method == "GET": 
            discount_list = models.DiscountInfo.objects.all() 
            context = { 
                "discount_list": discount_list, 
            }
            return render(request, "posapp/settings/discount_info.html", context) 
    else:
        return redirect("user_logout") 
    
    
def cancel_sales_order(request, invoice_num): 
    if request.session["userid"]: 
        if request.method == "GET": 
            models.SalesInfo.objects.filter(sales_invo = invoice_num).delete() 
            return redirect("sales_order_list") 
    else:
        return redirect("user_logout") 
    
def confirm_sales_order(request, invoice_num): 
    if request.session["userid"]: 
        if request.method == "GET": 
            sales_list = models.SalesInfo.objects.filter(sales_invo = invoice_num)
            total_price = 0
            for data in sales_list:
                total_price += data.unit_price + data.total_vat
                
            context = {
                "sales_invo": invoice_num,
                "total_price": total_price,
                "sales_list": sales_list
            }
            return render(request, "posapp/common/confirm_sales_order.html", context)
        else:
            payment_method = request.POST["payment_method"]
            card_number    = request.POST["card_number"]
            cash_amount    = int(float(request.POST["cash_amount"]))
            
            if len(card_number)==0:
                card_number = 0
            
            gift_card_amount = 0
            gift_card = models.GiftCard.objects.filter(card_number = card_number, status = True).first()
            if gift_card:
                gift_card_amount = gift_card.gift_amount
           
            total_amount = custom_tags.invoice_wise_grand_total(invoice_num)
             
            payment = models.SalesPaymentInfo.objects.create(
                sales_invo = invoice_num, total_amount = total_amount, cash_amount = cash_amount, gift_card_amount = gift_card_amount,
                card_number = card_number, payment_method = payment_method, confirm_by_id = request.session["userid"]
            )
            if payment:
                models.SalesInfo.objects.filter(sales_invo = invoice_num).update(sales_complete = True)
                models.GiftCard.objects.filter(card_number = card_number, status = True).update(status = False, used_date = datetime.now().date())
                
                sales_product = models.SalesInfo.objects.filter(sales_invo = invoice_num)
                for data in sales_product:
                    chk_exist = models.ProductInventory.objects.filter(product_cat_id = data.product_cat, product_brand_id = data.product_brand, product_name_id = data.product_name).first()
                    if chk_exist:
                        models.ProductInventory.objects.filter(pk = chk_exist.pk).update(current_quantity = F("current_quantity")-data.quantity)
                    
            return redirect("sales_order_list")    
    else:
        return redirect("user_logout") 
    
def generate_gift_card(request): 
    if request.session["userid"]: 
        if request.method == "GET": 
            return render(request, "posapp/settings/generate_gift_card.html")
        else:
            gift_amount   = int(request.POST["gift_amount"])
            card_quantity = int(request.POST["card_quantity"])
            
            card_number = 1000001
            max_card_number = models.GiftCard.objects.order_by("-card_number").first()
            if max_card_number:
                card_number = max_card_number.card_number+1
                    
            for data in range(card_quantity):
                chk_exist = models.GiftCard.objects.filter(card_number = card_number)
                if chk_exist:
                    card_number += 1
                else:    
                    models.GiftCard.objects.create(card_number = card_number, gift_amount = gift_amount)
                    card_number += 1
                
            return redirect("gift_card_list") 
    else:
        return redirect("user_logout") 
    
    
def gift_card_list(request): 
    if request.session["userid"]: 
        if request.method == "GET": 
            gift_card_list = models.GiftCard.objects.all()
            context = {
                "gift_card_list": gift_card_list
            }
            return render(request, "posapp/settings/gift_card_list.html", context)
    else:
        return redirect("user_logout") 
    
def inventory(request): 
    if request.session["userid"]: 
        if request.method == "GET": 
            inventory_list = models.ProductInventory.objects.order_by("product_name")
            product_list   = models.ProductInfo.objects.filter(status=True)
            context = { 
                "inventory_list": inventory_list,
                "product_list": product_list,
            }
            return render(request, "posapp/common/inventory.html", context)
        else: 
            product_name   = int(request.POST["product_name"])
            inventory_list = models.ProductInventory.objects.filter(product_name_id = product_name)
            product_list   = models.ProductInfo.objects.filter(status=True)
            context = { 
                "product_name": product_name,
                "inventory_list": inventory_list,
                "product_list": product_list,
            }
            return render(request, "posapp/common/inventory.html", context)
    else:
        return redirect("user_logout") 
    
def purchase_entry_by_ajax(request):
    if request.session["userid"]: 
        if request.is_ajax(): 
            product_cat     = request.POST.get("product_cat")
            product_brand   = request.POST.get("product_brand")
            product_name    = request.POST.get("product_name")
            quantity        = request.POST.get("quantity")
            unit_price      = request.POST.get("unit_price")
            sales_price     = request.POST.get("sales_price")
            purchase_invo   = request.POST.get("purchase_invo")
            purchase_date   = request.POST.get("purchase_date")
                         
            models.PurchaseInfo.objects.create(
                product_cat_id = product_cat, product_brand_id = product_brand, product_name_id = product_name, quantity = quantity,
                unit_price = unit_price, sales_price = sales_price, purchase_invo = purchase_invo, purchase_date = purchase_date, added_by_id = request.session["userid"]
            )
            
            chk_exist = models.ProductInventory.objects.filter(product_cat_id = product_cat, product_brand_id = product_brand, product_name_id = product_name).first()
            if chk_exist:
                models.ProductInventory.objects.filter(pk = chk_exist.pk).update(total_quantity = F("total_quantity")+quantity, current_quantity = F("current_quantity")+quantity)
            else:    
                models.ProductInventory.objects.create(
                    product_cat_id = product_cat, product_brand_id = product_brand, product_name_id = product_name,
                    total_quantity = quantity, current_quantity = quantity
                )
            return JsonResponse("Success", safe=False)
    else:
        return redirect("user_logout")         
              
def sales_entry_by_ajax(request):
    if request.session["userid"]: 
        if request.is_ajax(): 
            product_cat     = request.POST.get("product_cat")
            product_brand   = request.POST.get("product_brand")
            product_name    = request.POST.get("product_name")
            quantity        = request.POST.get("quantity")
            unit_price      = request.POST.get("unit_price").strip().split(" ") 
            sales_invo      = request.POST.get("sales_invo") 
            total_discount  = request.POST.get("total_discount")  
            
            if request.session["user_country"] == "USA":
                total_vat       = (((float(unit_price[1]) * float(quantity))-float(total_discount)) * 7.0)/100
            else:    
                total_vat       = (((float(unit_price[1]) * float(quantity))-float(total_discount)) * 5.0)/100                 
                             
            get_invo = models.SalesInfo.objects.create(
                product_cat_id = product_cat, product_brand_id = product_brand, product_name_id = product_name, quantity = quantity,
                unit_price = unit_price[1], total_vat = total_vat, sales_invo = sales_invo, sales_by_id = request.session["userid"]
            )
            if get_invo:
                chk_exist = models.InvoiceWiseDiscount.objects.filter(sales_invo = sales_invo)
                if chk_exist:
                    models.InvoiceWiseDiscount.objects.filter(sales_invo = sales_invo).update(total_discount = total_discount)
                else:
                    models.InvoiceWiseDiscount.objects.create(sales_invo = sales_invo, total_discount = total_discount)
                return JsonResponse("Success", safe=False)
            else: 
                return JsonResponse("Failed", safe=False)
    else:
        return redirect("user_logout")   
    
def get_product_salse_price_by_ajax(request):
    if request.is_ajax(): 
        product_id = request.GET.get("product_id")
        product_cat = request.GET.get("product_cat")
        product_brand = request.GET.get("product_brand")
        get_price = models.PurchaseInfo.objects.filter(product_cat_id = product_cat, product_brand_id = product_brand, product_name_id = product_id).first()
        
        if get_price:
            sales_price = get_price.sales_price
        else:
            sales_price = 0
            
        if request.session["user_country"] == "USA":    
            sales_price = custom_tags.bdt_to_usd(sales_price) 
            return JsonResponse(str(sales_price), safe=False) 
        else:
            return JsonResponse(str(sales_price), safe=False) 
    
def discount_calculation_by_ajax(request):
    if request.is_ajax(): 
        sub_total  = request.POST.get("sub_total")  
        current_month = datetime.now().date()
        get_discount = models.DiscountInfo.objects.filter(from_month__lte = current_month, to_month__gte = current_month, country_name__country_name = request.session["user_country"], from_amount__lte = sub_total, status=True).order_by("-from_amount").first()

        if get_discount:
            discount = get_discount.discount
        else:
            discount = 0
        return JsonResponse(str(discount), safe=False)
    
def check_valid_gift_card_number_by_ajax(request):
    if request.is_ajax(): 
        card_number  = request.GET.get("card_number")  
        chk_valid_card = models.GiftCard.objects.filter(card_number = card_number, status=True).first()

        if chk_valid_card:
            return JsonResponse(str(chk_valid_card.gift_amount), safe=False)
        else:
            return JsonResponse(str(0), safe=False)
        
            
