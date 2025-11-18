from django.contrib import messages
from .models import Product, Profile, SalesRecord, Staff
from django.shortcuts import get_object_or_404, redirect, render
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
    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get("product_id")   # FIXED
        quantity = int(request.POST.get("quantity"))
        customer = request.POST.get("customer_name")

        # Validate product
        product = get_object_or_404(Product, id=product_id)

        # Check stock
        if quantity > product.quantity:
            return render(request, "staff/record_sales.html", {
                "products": products,
                "error": "Not enough stock available!"
            })

        # Reduce stock
        product.quantity -= quantity
        product.save()

        # Save sales record
        SalesRecord.objects.create(
            product=product,
            quantity=quantity,
            customer_name=customer,
            staff=request.user
        )

        return redirect("view_sales")

    return render(request, "staff/record_sales.html", {
        "products": products
    })


def view_sales(request):
    sales = SalesRecord.objects.all().order_by("-date")
    return render(request, "staff/view_sales.html", {"sales": sales})


def products(request):
    search_query = request.GET.get("search", "")
    selected_category = request.GET.get("category", "")

    products = Product.objects.all()

    # search
    if search_query:
        products = products.filter(name__icontains=search_query)

    # filter category
    if selected_category:
        products = products.filter(category=selected_category)

    categories = Product.objects.values_list("category", flat=True).distinct()
    return render(request,'staff/products.html', {
        "products": products,
        "categories": categories,
        "search_query": search_query,
        "selected_category": selected_category,
    })



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
        # experience = request.POST.get("experience")

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
    total_products = Product.objects.count()

    low_stock_threshold = 20
    low_stock_count = Product.objects.filter(quantity__lte=low_stock_threshold).count()

    staff_count = Staff.objects.count()

    
    return render(request,'admin/admin_dashboard.html', {
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "staff_count": staff_count,
    })

def add_products(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")

        # Save to DB
        Product.objects.create(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
        )

        messages.success(request, "Product added successfully!")
        return redirect("view_products")
    return render(request,'admin/add_products.html')



def view_products(request):
    products = Product.objects.all().order_by('name')   # show alphabetically
    total_products = products.count()

    # Optional: Count low-stock items (ex: quantity <= 5)
    low_stock_threshold = 20
    low_stock_count = Product.objects.filter(quantity__lte=low_stock_threshold).count()

    context = {
        "products": products,
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "low_stock_threshold": low_stock_threshold,
    }

    return render(request,'admin/view_products.html', context)

def low_stock(request):
     # Set low stock limit
    low_stock_threshold = 20

    # Fetch items at or below threshold
    low_stock_items = Product.objects.filter(quantity__lte=low_stock_threshold).order_by('quantity')

    context = {
        "low_stock": low_stock_items,
        "low_stock_threshold": low_stock_threshold,
    }

    return render(request,'admin/low_stock.html', context)

def staff_management(request):
    staff_list = Staff.objects.all()
    staff_count = staff_list.count()

    context = {
        "staff_list": staff_list,
        "staff_count": staff_count,
    }
    return render(request,'admin/staff_management.html', context)



def staff_edit(request,staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == "POST":
        staff.full_name = request.POST.get("full_name")
        staff.dob = request.POST.get("dob")
        staff.age = request.POST.get("age")
        staff.gender = request.POST.get("gender")
        staff.phone = request.POST.get("phone")
        staff.address = request.POST.get("address")
        staff.department = request.POST.get("department")
        staff.job_title = request.POST.get("job_title")
        staff.start_date = request.POST.get("start_date")
        staff.is_active = True if request.POST.get("is_active") == "on" else False

        staff.save()
        messages.success(request, "Staff details updated successfully!")
        return redirect("staff_management")

    
    return render(request,'admin/staff_edit.html',{'staff':staff})


def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    staff.profile.user.delete()
    return redirect("staff_management")

def restock_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        qty = int(request.POST.get("quantity"))
        product.quantity += qty
        product.save()
        return redirect("low_stock")
    return render(request,'admin/restock_product.html', {"product": product})



