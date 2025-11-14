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
    profile_pic = models.ImageField(upload_to='profile_pics/',default='default.jpg')
    def __str__(self):
        return f"{self.user.username} {self.role}"
    
