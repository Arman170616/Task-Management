from django.urls import path
from .views import user_registration, user_login, create_task, get_all_tasks, get_task, update_task, delete_task, get_all_users, get_user, sort_tasks, filter_tasks, create_comment, get_all_comments, get_comment, update_comment, delete_comment

urlpatterns = [
    path('register/', user_registration, name='user-registration'),
    path('login/', user_login, name='user-login'),

    path('tasks/', create_task, name='create-task'),
    path('pagination/', get_all_tasks, name='get-all-tasks'),
    
    path('get-task/<int:task_id>/', get_task, name='get-task'),
    path('update-task/<int:task_id>/', update_task, name='update-task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete-task'),

    path('users/', get_all_users, name='get-all-users'),
    path('users/<int:user_id>/', get_user, name='get-user'),

    path('filter-tasks/', filter_tasks, name='filter-tasks'),
    path('tasks/sort/', sort_tasks, name='sort-tasks'),


    path('tasks/<int:task_id>/comments/', create_comment, name='create-comment'),
    path('get-all-tasks/<int:task_id>/comments/', get_all_comments, name='get-all-comments'),
    path('get-comment/<int:comment_id>/', get_comment, name='get-comment'),
    path('update-comment/<int:comment_id>/', update_comment, name='update-comment'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete-comment'),




]
