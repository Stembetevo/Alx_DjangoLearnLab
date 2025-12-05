from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = list(UserAdmin.fieldsets) + [
        ('Additional', {'fields': ('date_of_birth', 'profile_photo')}),
    ]

admin.site.register(CustomUser, CustomUserAdmin)