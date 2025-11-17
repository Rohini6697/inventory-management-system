from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ROLE_CHOICES = (
        ('manager','Manager'),
        ('staff','Staff'),
        ('accountant','Accountant')
    )
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='staff')
    profile_pic = models.ImageField(upload_to='profile_pics/',default='profile_pics/default.jpg')
    def __str__(self):
        return f"{self.user.username} {self.role}"
    





class Staff(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="staff")

    # Personal Information
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField()

    gender = models.CharField(
        max_length=10,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )

    # Contact Information
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # Work Details
    department = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.full_name} ({self.profile.user.username})"





class Product(models.Model):

    # 1. Product Image
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # 2. Product Identification
    category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True, null=True)
    # sku = models.CharField(max_length=100, unique=True)   # product code / SKU
    model_number = models.CharField(max_length=100, blank=True, null=True)

    # 3. Description
    description = models.TextField(blank=True, null=True)

    # 4. Pricing
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # 5. Stock Info
    stock_quantity = models.PositiveIntegerField(default=0)
    alert_stock = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=150, blank=True, null=True)

    # 6. Lifecycle
    manufacturing_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    warranty_period = models.PositiveIntegerField(blank=True, null=True)   # in months
    warranty_end = models.DateField(blank=True, null=True)

    # 7. Supplier Info
    supplier_name = models.CharField(max_length=150, blank=True, null=True)
    supplier_contact = models.CharField(max_length=50, blank=True, null=True)
    supplier_address = models.TextField(blank=True, null=True)

    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name





class SalesRecord(models.Model):
    sale_date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    customer_name = models.CharField(max_length=150, blank=True, null=True)

    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale - {self.product.name} - {self.sale_date}"
