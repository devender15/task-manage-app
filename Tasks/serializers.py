from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'description', 'status', 'due_date', 'userId')
    
    def create(self, validated_data):
        userId = self.context.get('user_id')
        task = Task.objects.create(name=validated_data['name'], userId=userId, description=validated_data['description'], status=validated_data['status'], due_date=validated_data['due_date'])
        return task

