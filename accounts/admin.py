from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ApplicantProfile, EmployerProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_staff', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'profile_picture', 'bio')}),
    )

@admin.register(ApplicantProfile)
class ApplicantProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'linkedin', 'portfolio']
    search_fields = ['user__username', 'skills']

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'location', 'website']
    search_fields = ['company_name', 'location']