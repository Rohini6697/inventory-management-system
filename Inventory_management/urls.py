from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('',views.signup,name = 'signup'),
    path('signin/',views.signin,name = 'signin'),
    # path('/signin',views.signin,name = 'signin'),





# =============================  MANAGER  ====================================
path('manager_dashboard/',views.manager_dashboard,name = 'manager_dashboard'),


# =============================  STAFF  ====================================
path('staff_dashboard/',views.staff_dashboard,name = 'staff_dashboard'),
path('staff_profile/',views.staff_profile,name = 'staff_profile'),
path('record_sales/',views.record_sales,name = 'record_sales'),
path('view_sales/',views.view_sales,name = 'view_sales'),
path('products/',views.products,name = 'products'),
path('add_products/',views.add_products,name = 'add_products'),
path('add_details/',views.add_details,name = 'add_details'),
path('staff_details/',views.staff_details,name = 'staff_details'),





# =============================  Accountant  ====================================
path('accountant_dashboard/',views.accountant_dashboard,name = 'accountant_dashboard'),



# =============================  Admin  ====================================
path('admin_dashboard/',views.admin_dashboard,name = 'admin_dashboard'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
