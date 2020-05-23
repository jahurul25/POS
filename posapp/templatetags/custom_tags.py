from django import template  
import requests

register = template.Library()


@register.filter(name='subtract')
def subtract(value1, value2):
    return value1 - value2


@register.filter(name='bdt_to_usd')
def bdt_to_usd(bdt):
    r = requests.get('http://data.fixer.io/api/convert?access_key=29dcdbbac1fb5048f47fec7c7a05b5cb&from=BDT&to=USD&amount="'+bdt+'"')
    # usd = r.json()["rates"]["USD"]
    usd = r.json()
    
    print("rate: ", usd)
    return usd


