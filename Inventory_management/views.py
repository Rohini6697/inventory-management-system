from .models import Profile
from django.shortcuts import redirect, render
from .forms import UserForm,ProfileForm
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES) 
        if form.is_valid() and profile_form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.role = form.cleaned_data['role']   # save the role here
            profile.save()

            return redirect('signin')

    else:
        form = UserForm()
        profile_form = ProfileForm()
    return render(request,'signup.html',{'form':form,'profile_form': profile_form   })
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username,password = password)
        if user is not None:
            auth_login(request,user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                role = user.profile.role
                if role == 'manager':
                    return redirect('manager_dashboard')
                elif role == 'staff':
                    return redirect('staff_dashboard')
                elif role == 'accountant':
                    return redirect('accountant_dashboard')

    
    return render(request,'signin.html')


# ==========================================  MANAGER   ==========================================
def manager_dashboard(request):
    return render(request,'manager/manager_dashboard.html')

# ==========================================  STAFF   ==========================================
def staff_dashboard(request):
    return render(request,'staff/staff_dashboard.html')

def staff_profile(request):
    return render(request,'staff/staff_profile.html')

def record_sales(request):
    return render(request,'staff/record_sales.html')

def view_sales(request):
    return render(request,'staff/view_sales.html')

def products(request):
    return render(request,'staff/products.html')



# ==========================================  ACCOUNTANT   ==========================================
def accountant_dashboard(request):
    return render(request,'accountant/accountant_dashboard.html')

# ==========================================  ADMIN   ==========================================
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')






