from django.contrib import admin

from .models import Task, TaskComment, CustomUser
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskComment)
admin.site.register(CustomUser)

