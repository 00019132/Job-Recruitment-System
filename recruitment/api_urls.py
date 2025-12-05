from django.urls import path
from rest_framework.routers import DefaultRouter
from .views_api import JobViewSet, ApplicationViewSet, InterviewViewSet  # Define these below

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'interviews', InterviewViewSet)

urlpatterns = router.urls