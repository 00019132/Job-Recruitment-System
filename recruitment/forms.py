
from django import forms
from .models import Job, Application, Interview

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 'job_type', 'salary_range', 'deadline', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., $50,000 - $70,000'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'class': 'form-control', 'placeholder': 'Tell us why you\'re a great fit...'}),
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['scheduled_date', 'location', 'notes']
        widgets = {
            'scheduled_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Office address or video call link'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }