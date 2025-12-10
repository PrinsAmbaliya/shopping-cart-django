# Ecommerce/admin.py

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# 1. Unregister the default UserAdmin
admin.site.unregister(User)

# 2. Define your custom UserAdmin class
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'is_active', 'date_joined'
    )
    fieldsets = (
        (None, {'fields': ('username', 'password', 'id')}), # Added 'id' here
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    readonly_fields = ('id', 'date_joined', 'last_login',)


admin.site.register(User, CustomUserAdmin)