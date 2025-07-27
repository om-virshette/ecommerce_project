from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import the CustomUser model

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'contact_number', 'address', 'profile_picture', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'contact_number', 'address', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'contact_number', 'address', 'profile_picture', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ['email', 'username', 'contact_number']
    ordering = ['email']

# Register the custom user model and admin customization
admin.site.register(CustomUser, CustomUserAdmin)
