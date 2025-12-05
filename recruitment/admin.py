
from django.contrib import admin
from .models import Job, Application, Interview

class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0
    readonly_fields = ['applicant', 'applied_at']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'job_type', 'location', 'is_active', 'created_at']
    list_filter = ['job_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'location']
    inlines = [ApplicationInline]

class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 0

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__username', 'job__title']
    inlines = [InterviewInline]

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['application', 'scheduled_date', 'is_completed']
    list_filter = ['is_completed', 'scheduled_date']
    search_fields = ['application__applicant__username', 'application__job__title']
