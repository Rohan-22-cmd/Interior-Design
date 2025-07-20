from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    
    # Customize fieldsets by removing the duplicate 'email' field
    fieldsets = (
        # Keep all default fieldsets from UserAdmin, excluding email
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        # Add fields for creating a new user (without duplicating 'email')
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
