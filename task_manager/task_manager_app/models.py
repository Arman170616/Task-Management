from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings


class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.task_name


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on Task '{self.task.task_name}'"


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('team_member', 'Team Member'),
    )

    user_role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='team_member'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
