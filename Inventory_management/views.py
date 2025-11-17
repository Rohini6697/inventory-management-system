from .models import Product, Profile, Staff
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
                    try:
                        staff = user.profile.staff
                        return redirect('staff_dashboard')
                    except Staff.DoesNotExist:
                        return redirect('staff_details')
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

def add_products(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        category = request.POST.get('category')
        product_name = request.POST.get('product_name')
        brand = request.POST.get('brand')
        sku = request.POST.get('sku')
        model_number = request.POST.get('model_number')

        description = request.POST.get('description')

        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')
        discount = request.POST.get('discount')
        discounted_price = request.POST.get('discounted_price')

        stock_quantity = request.POST.get('stock_quantity')
        alert_stock = request.POST.get('alert_stock')
        location = request.POST.get('location')

        manufacturing_date = request.POST.get('manufacturing_date')
        purchase_date = request.POST.get('purchase_date')
        warranty_period = request.POST.get('warranty_period')
        warranty_end = request.POST.get('warranty_end')

        supplier_name = request.POST.get('supplier_name')
        supplier_contact = request.POST.get('supplier_contact')
        supplier_address = request.POST.get('supplier_address')

        Product.objects.create(
            image=image,
            category=category,
            product_name=product_name,
            brand=brand,
            sku=sku,
            model_number=model_number,
            description=description,
            cost_price=cost_price,
            selling_price=selling_price,
            discount=discount,
            discounted_price=discounted_price,
            stock_quantity=stock_quantity,
            alert_stock=alert_stock,
            location=location,
            manufacturing_date=manufacturing_date,
            purchase_date=purchase_date,
            warranty_period=warranty_period,
            warranty_end=warranty_end,
            supplier_name=supplier_name,
            supplier_contact=supplier_contact,
            supplier_address=supplier_address,
        )

        return redirect("view_sales")  
    return render(request,'staff/add_products.html')

def add_details(request):
    return render(request,'staff/add_details.html')

def staff_details(request):
    profile = request.user.profile  
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        dob = request.POST.get("dob")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        department = request.POST.get("department")
        job_title = request.POST.get("job_title")
        start_date = request.POST.get("start_date")
        experience = request.POST.get("experience")

        Staff.objects.create(
            profile=profile,
            full_name=full_name,
            dob=dob,
            age=age,
            gender=gender,
            phone=phone,
            address=address,
            department=department,
            job_title=job_title,
            start_date=start_date,
        )

        return redirect("staff_dashboard")
    return render(request,'staff/staff_details.html')




# ==========================================  ACCOUNTANT   ==========================================
def accountant_dashboard(request):
    return render(request,'accountant/accountant_dashboard.html')

# ==========================================  ADMIN   ==========================================
def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')






