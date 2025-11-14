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
            profile.save()

            role = request.POST.get('role')
            Profile.objects.create(user = user, role = form.cleaned_data['role'])
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
    return render(request,'staff_dashboard.html')

# ==========================================  ACCOUNTANT   ==========================================
def accountant_dashboard(request):
    return render(request,'accountant_dashboard.html')

# ==========================================  ADMIN   ==========================================
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')






