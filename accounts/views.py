from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ApplicantProfileForm, EmployerProfileForm
from .models import ApplicantProfile, EmployerProfile

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'applicant':
                ApplicantProfile.objects.create(user=user)
            elif user.role == 'employer':
                EmployerProfile.objects.create(user=user, company_name=f"{user.username}'s Company")
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('recruitment:dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    profile_form = None
    
    if user.role == 'applicant':
        profile = getattr(user, 'applicant_profile', None)
        if not profile:
            profile = ApplicantProfile.objects.create(user=user)
        if request.method == 'POST':
            profile_form = ApplicantProfileForm(request.POST, request.FILES, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        else:
            profile_form = ApplicantProfileForm(instance=profile)
    elif user.role == 'employer':
        profile = getattr(user, 'employer_profile', None)
        if not profile:
            profile = EmployerProfile.objects.create(user=user, company_name=f"{user.username}'s Company")
        if request.method == 'POST':
            profile_form = EmployerProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        else:
            profile_form = EmployerProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'profile_form': profile_form, 'user': user})

