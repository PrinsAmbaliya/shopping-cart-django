# Ecommerce/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin # <--- Make sure this is imported

# 1. Unregister the default UserAdmin
admin.site.unregister(User)

# 2. Define your custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    # 'id' is added here!
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'is_active', 'date_joined'
    )

# 3. Re-register the User model with your custom admin class
admin.site.register(User, CustomUserAdmin)