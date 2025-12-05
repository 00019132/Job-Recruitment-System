from rest_framework import serializers
from .models import Job, Application, Interview
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class JobSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer', 'created_at', 'updated_at']

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['applicant', 'applied_at', 'updated_at']

class InterviewSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)
    
    class Meta:
        model = Interview
        fields = '__all__'
        read_only_fields = ['created_at']