from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.signup,name = 'signup'),
    path('signin/',views.signin,name = 'signin'),
    # path('/signin',views.signin,name = 'signin'),





# =============================  MANAGER  ====================================
path('manager_dashboard/',views.manager_dashboard,name = 'manager_dashboard'),


# =============================  STAFF  ====================================
path('staff_dashboard/',views.staff_dashboard,name = 'staff_dashboard'),




# =============================  Accountant  ====================================
path('accountant_dashboard/',views.accountant_dashboard,name = 'accountant_dashboard'),



# =============================  Admin  ====================================
path('admin_dashboard/',views.admin_dashboard,name = 'admin_dashboard'),



]

