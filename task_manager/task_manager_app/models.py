from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on Task '{self.task.task_name}'"