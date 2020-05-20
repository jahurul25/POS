from django.urls import path, include
from posapp import views
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('user-profile/', views.user_profile, name="user_profile"),
    path('user-list/', views.user_list, name="user_list"),
    path('settings/country-list/', views.country_list, name="country_list"),
    path('settings/year-list/', views.year_list, name="year_list"),
    path('settings/company-setup/', views.company_setup, name="company_setup"),
    path('purchase-entry/', views.purchase_entry, name="purchase_entry"),
    path('sales-entry/', views.sales_entry, name="sales_entry"),
    path('inventory/', views.inventory, name="inventory"),
]

