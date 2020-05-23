from django import template  
import requests

register = template.Library()


@register.filter(name='subtract')
def subtract(value1, value2):
    return value1 - value2


@register.filter(name='bdt_to_usd')
def bdt_to_usd(sub_total):
    response = requests.post('http://data.fixer.io/api/latest?access_key=e7546ef7cada53aeea71524d9176e113&format=1') 
    if response.status_code == 200:
        data = response.json()
        usd = round((sub_total/data["rates"]["BDT"])/data["rates"]["USD"]) 
        return usd 
    else: sub_total
