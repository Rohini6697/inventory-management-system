from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'profile_image')

    def profile_image(self, obj):
        if obj.profile_pic:
            return f"<img src='{obj.profile_pic.url}' width='50' height='50' />"
        return "No Image"
    
    profile_image.allow_tags = True

admin.site.register(Profile, ProfileAdmin)
