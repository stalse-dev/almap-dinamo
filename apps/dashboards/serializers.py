from rest_framework import serializers
from apps.dashboards.models import Dashboard, WorkSpace

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'

class DashboardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ['id', 'title', 'embed_url', 'description']

class WorkSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'dashboards', 'users']
        
        
class WorkSpaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpace
        fields = ['id', 'name', 'description', 'tags', 'dashboards', 'users']