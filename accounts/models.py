from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class ApplicantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, help_text="Comma-separated skills")
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=200)
    
    def __str__(self):
        return self.company_name
