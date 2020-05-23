from django.urls import path, include
from posapp import views
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"), 
    path('dashboard/', views.dashboard, name="dashboard"),
    path('user-profile/', views.user_profile, name="user_profile"),
    path('user-list/', views.user_list, name="user_list"),
    path('user-registration/', views.user_registration, name="user_registration"),
    path('settings/country-list/', views.country_list, name="country_list"),
    path('settings/year-list/', views.year_list, name="year_list"),
    path('settings/company-setup/', views.company_setup, name="company_setup"),
    path('settings/add-product-category/', views.add_product_category, name="add_product_category"),
    path('settings/product-category-list/', views.product_category_list, name="product_category_list"),
    path('settings/add-product-brand/', views.add_product_brand, name="add_product_brand"),
    path('settings/product-brand-list/', views.product_brand_list, name="product_brand_list"),
    path('settings/add-product-name/', views.add_product_name, name="add_product_name"),
    path('settings/product-name-list/', views.product_name_list, name="product_name_list"),
    path('purchase-entry/', views.purchase_entry, name="purchase_entry"),
    path('purchase-list/', views.purchase_list, name="purchase_list"),
    path('sales-entry/', views.sales_entry, name="sales_entry"),
    path('sales-list/', views.sales_list, name="sales_list"),
    path('sales-order-list/', views.sales_order_list, name="sales_order_list"),
    path('inventory/', views.inventory, name="inventory"),
    path('settings/discount-info/', views.discount_info, name="discount_info"),
    
    path('ajax/purchase-entry/', views.purchase_entry_by_ajax, name="purchase_entry_by_ajax"),
    path('ajax/sales-entry/', views.sales_entry_by_ajax, name="sales_entry_by_ajax"),
    path('ajax/get-product-salse-price/', views.get_product_salse_price_by_ajax, name="get_product_salse_price_by_ajax"),
    path('ajax/discount-calculation/', views.discount_calculation_by_ajax, name="discount_calculation_by_ajax"),
]

