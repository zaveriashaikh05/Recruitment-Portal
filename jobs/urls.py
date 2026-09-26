from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('register/', views.candidate_register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='jobs/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='login'
        ),
        name='logout'
    ),

    path(
        'apply/<int:job_id>/',
         views.apply_job,
         name='apply_job'
         ),
    path(
    'my-applications/',
    views.my_applications,
    name='my_applications'
         ),
    path(
        'search/', views.search_jobs, name='search_jobs'
        ),
        path(
            'dashboard/', views.admin_dashboard, name='admin_dashboard'
            ),
]