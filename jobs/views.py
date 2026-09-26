from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobApplicationForm
from .models import Application
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CandidateRegistrationForm
from .models import CandidateProfile, Job


def candidate_register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            CandidateProfile.objects.create(
                user=user,
                phone='',
            )

            login(request, user)
            return redirect('job_list')

    else:
        form = CandidateRegistrationForm()

    return render(
        request,
        'jobs/register.html',
        {'form': form}
    )
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')

    return render(
        request,
        'jobs/job_list.html',
        {'jobs': jobs}
    )
@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(
        candidate=request.user,
        job=job
    ).exists():
        return redirect('job_list')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = request.user
            application.job = job
            application.save()

            return redirect('job_list')
    else:
        form = JobApplicationForm()

    return render(
        request,
        'jobs/apply_job.html',
        {'form': form, 'job': job}
    )
@login_required
def my_applications(request):
    applications = Application.objects.filter(
        candidate=request.user
    )
    print("CURRENT USER:", request.user, flush=True)
    print("APPLICATION COUNT:", applications.count(), flush=True)
    return render(
        request,
        'jobs/my_applications.html',
        {'applications': applications}
    )

from django.db.models import Q

def search_jobs(request):
    query = request.GET.get('q', '')

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        )

    return render(
        request,
        'jobs/job_list.html',
        {
            'jobs': jobs,
            'query': query
        }
    )

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard(request):
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()

    shortlisted = Application.objects.filter(
        status='Shortlisted'
    ).count()

    interviews = Application.objects.filter(
        status='Interview'
    ).count()

    context = {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'interviews': interviews,
    }

    return render(
        request,
        'jobs/admin_dashboard.html',
        context
    )
