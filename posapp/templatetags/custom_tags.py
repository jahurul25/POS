from django import template  
from posapp import models
from django.db.models import Count, Sum
import requests

register = template.Library()


@register.filter(name='subtract')
def subtract(value1, value2):
    return value1 - value2

@register.filter(name='get_total_discount')
def get_total_discount(invoice_number):
    discount = models.InvoiceWiseDiscount.objects.filter(sales_invo = invoice_number).first()
    if discount:
        return discount.total_discount
    else:
        return 0  


@register.filter(name='invoice_wise_grand_total')
def invoice_wise_grand_total(invoice_number):
    discount = models.InvoiceWiseDiscount.objects.filter(sales_invo = invoice_number).first()
    total_discount = 0
    if discount:
        total_discount = discount.total_discount
    
    grand_total = 0 
    get_sub_total = models.SalesInfo.objects.filter(sales_invo = invoice_number, sales_complete=False)  
    for data in get_sub_total:
        grand_total += ((data.unit_price*data.quantity)+data.total_vat)
        
    return grand_total-total_discount    

@register.filter(name='bdt_to_usd')
def bdt_to_usd(sub_total):
    response = requests.post('http://data.fixer.io/api/latest?access_key=e7546ef7cada53aeea71524d9176e113&format=1') 
    if response.status_code == 200:
        data = response.json()
        usd = round((sub_total/data["rates"]["BDT"])*data["rates"]["USD"]) 
        print("sub_total: ", sub_total)
        print("BDT:", data["rates"]["BDT"])
        print("USD:", data["rates"]["USD"])
        print("usd: ", usd)
        return usd 
    else: sub_total

