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

    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


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
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name





class SalesRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=150, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
