
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_api import JobViewSet, ApplicationViewSet, InterviewViewSet

app_name = 'recruitment'

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='job-api')
router.register('applications', ApplicationViewSet, basename='application-api')
router.register('interviews', InterviewViewSet, basename='interview-api')

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs/<int:pk>/update/', views.job_update, name='job_update'),
    path('jobs/<int:pk>/delete/', views.job_delete, name='job_delete'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('jobs/<int:pk>/applications/', views.job_applications, name='job_applications'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/update-status/', views.update_application_status, name='update_status'),
    path('applications/<int:pk>/schedule-interview/', views.schedule_interview, name='schedule_interview'),
    path('api/', include(router.urls)),
]