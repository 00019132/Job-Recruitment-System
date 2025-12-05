from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Job, Application, Interview
from .serializers import JobSerializer, ApplicationSerializer, InterviewSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.filter(is_active=True)
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)
    
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        job = self.get_object()
        applications = Application.objects.filter(job=job)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'applicant':
            return Application.objects.filter(applicant=user)
        elif user.role == 'employer':
            return Application.objects.filter(job__employer=user)
        return Application.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'applicant':
            return Interview.objects.filter(application__applicant=user)
        elif user.role == 'employer':
            return Interview.objects.filter(application__job__employer=user)
        return Interview.objects.all()