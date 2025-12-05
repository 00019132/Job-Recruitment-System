
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ApplicantProfile, EmployerProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'phone')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [('applicant', 'Applicant'), ('employer', 'Employer')]
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        fields = ['resume', 'skills', 'education', 'experience', 'linkedin', 'portfolio']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'education': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'portfolio': forms.URLInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'website', 'location']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }