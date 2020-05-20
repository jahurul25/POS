from django.shortcuts import render, redirect
from posapp import models
from django.http import JsonResponse
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
            chk_user_login = models.UserList.objects.filter(user_email=user_email, user_pass=encrypt_pass, status=True)
            if chk_user_login:
                return redirect("/dashboard/")
            else:
                return render(request, "posapp/common/user_login.html")
    # except:
    #     return redirect("/login/")  

def user_logout(request):
    return redirect("/login/")
    

def dashboard(request):
    dt = models.CountryList.objects.all()
    print("dashboard: ", dt)
    return render(request, "posapp/common/dashboard.html")

def user_profile(request):
    dt = models.CountryList.objects.all()
    print("dashboard: ", dt)
    return render(request, "posapp/common/user_profile.html")

def user_list(request):
    dt = models.CountryList.objects.all() 
    return render(request, "posapp/settings/user_list.html")


def country_list(request): 
    return render(request, "posapp/settings/country_list.html")


def year_list(request): 
    return render(request, "posapp/settings/year_list.html")

def company_setup(request): 
    return render(request, "posapp/settings/company_setup.html")

def purchase_entry(request): 
    return render(request, "posapp/common/purchase_entry.html")

def sales_entry(request): 
    return render(request, "posapp/common/sales_entry.html")

def inventory(request): 
    return render(request, "posapp/common/inventory.html")

