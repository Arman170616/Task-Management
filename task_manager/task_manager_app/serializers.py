from rest_framework import serializers
from .models import Task, TaskComment
from django.contrib.auth.models import User
from django.utils import timezone


# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = ['id', 'task_name', 'description', 'due_date', 'assignee']



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_name', 'description', 'due_date', 'assignee']

    def validate_due_date(self, value):
        # Add custom validation logic for due_date field
        # For example, ensure that the due_date is in the future
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['id', 'comment', 'created_at']