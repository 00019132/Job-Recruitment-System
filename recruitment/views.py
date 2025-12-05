from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Job, Application, Interview
from .forms import JobForm, ApplicationForm, ApplicationStatusForm, InterviewForm

@login_required
def dashboard(request):
    user = request.user
    
    if user.is_staff or user.role == 'admin':
        from django.shortcuts import redirect
        return redirect('/admin/')
    
    context = {'user': user}
    
    if user.role == 'applicant':
        context['applications'] = Application.objects.filter(applicant=user).select_related('job')[:5]
        context['interviews'] = Interview.objects.filter(application__applicant=user).select_related('application__job')[:5]
        context['available_jobs'] = Job.objects.filter(is_active=True).exclude(applications__applicant=user)[:5]
    elif user.role == 'employer':
        context['jobs'] = Job.objects.filter(employer=user).annotate(app_count=Count('applications'))[:5]
        context['recent_applications'] = Application.objects.filter(job__employer=user).select_related('job', 'applicant')[:5]
        context['interviews'] = Interview.objects.filter(application__job__employer=user).select_related('application')[:5]
    
    return render(request, 'recruitment/dashboard.html', context)

@login_required
def job_list(request):
    jobs = Job.objects.filter(is_active=True).select_related('employer')
    search = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    
    if search:
        jobs = jobs.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(location__icontains=search))
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    return render(request, 'recruitment/job_list.html', {'jobs': jobs, 'search': search, 'job_type': job_type})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.role == 'applicant':
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'recruitment/job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
def job_create(request):
    if request.user.role != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('recruitment:dashboard')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('recruitment:job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'recruitment/job_form.html', {'form': form, 'action': 'Create'})

@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('recruitment:job_detail', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'recruitment/job_form.html', {'form': form, 'action': 'Update'})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('recruitment:my_jobs')
    return render(request, 'recruitment/job_confirm_delete.html', {'job': job})

@login_required
def my_jobs(request):
    if request.user.role != 'employer':
        return redirect('recruitment:dashboard')
    jobs = Job.objects.filter(employer=request.user).annotate(app_count=Count('applications'))
    return render(request, 'recruitment/my_jobs.html', {'jobs': jobs})

@login_required
def apply_job(request, pk):
    if request.user.role != 'applicant':
        messages.error(request, 'Only applicants can apply for jobs.')
        return redirect('recruitment:job_detail', pk=pk)
    
    job = get_object_or_404(Job, pk=pk, is_active=True)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('recruitment:job_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('recruitment:my_applications')
    else:
        form = ApplicationForm()
    return render(request, 'recruitment/apply_job.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    if request.user.role != 'applicant':
        return redirect('recruitment:dashboard')
    applications = Application.objects.filter(applicant=request.user).select_related('job')
    return render(request, 'recruitment/my_applications.html', {'applications': applications})

@login_required
def job_applications(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    applications = Application.objects.filter(job=job).select_related('applicant')
    return render(request, 'recruitment/job_applications.html', {'job': job, 'applications': applications})

@login_required
def application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.user.role == 'employer' and application.job.employer != request.user:
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('recruitment:dashboard')
    if request.user.role == 'applicant' and application.applicant != request.user:
        messages.error(request, 'You do not have permission to view this application.')
        return redirect('recruitment:dashboard')
    
    interviews = Interview.objects.filter(application=application)
    return render(request, 'recruitment/application_detail.html', {'application': application, 'interviews': interviews})

@login_required
def update_application_status(request, pk):
    application = get_object_or_404(Application, pk=pk, job__employer=request.user)
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application status updated!')
            return redirect('recruitment:application_detail', pk=pk)
    else:
        form = ApplicationStatusForm(instance=application)
    return render(request, 'recruitment/update_status.html', {'form': form, 'application': application})

@login_required
def schedule_interview(request, pk):
    application = get_object_or_404(Application, pk=pk, job__employer=request.user)
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            application.status = 'interview'
            application.save()
            messages.success(request, 'Interview scheduled successfully!')
            return redirect('recruitment:application_detail', pk=pk)
    else:
        form = InterviewForm()
    return render(request, 'recruitment/schedule_interview.html', {'form': form, 'application': application})

