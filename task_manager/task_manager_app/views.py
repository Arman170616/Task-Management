from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth.models import User
from .serializers import UserSerializer


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, TaskComment
from .serializers import TaskSerializer, TaskCommentSerializer, UserSerializer

from .decorators import role_required


@api_view(['POST'])
def user_registration(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if the username or password is missing
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username is already taken
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user account
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()

    # Generate JWT
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token

    # Return the JWT in the response
    return Response({
        'message': 'User registered successfully.',
        'access_token': str(access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def user_login(request):
    # Delegate the login logic to the built-in TokenObtainPairView from SimpleJWT
    return TokenObtainPairView.as_view()(request)


# @api_view(['POST'])
# def create_task(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['PUT'])
# def update_task(request, task_id):
#     try:
#         task = Task.objects.get(id=task_id)
#     except Task.DoesNotExist:
#         return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = TaskSerializer(task, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def create_task(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def update_task(request, task_id):
#     try:
#         task = Task.objects.get(id=task_id)
#     except Task.DoesNotExist:
#         return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = TaskSerializer(task, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def get_all_tasks(request):
#     tasks = Task.objects.all()
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)

class TaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET'])
def get_all_tasks(request):
    paginator = TaskPagination()
    tasks = Task.objects.all()
    page = paginator.paginate_queryset(tasks, request)
    serializer = TaskSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def get_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(task)
    return Response(serializer.data)



@api_view(['DELETE'])
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)
    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
def filter_tasks(request):
    assignee = request.GET.get('assignee')
    completed = request.GET.get('completed')
    due_date = request.GET.get('due_date')

    tasks = Task.objects.all()

    if assignee:
        tasks = tasks.filter(assignee__username=assignee)

    if completed:
        tasks = tasks.filter(completed=completed)

    if due_date:
        tasks = tasks.filter(due_date=due_date)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def sort_tasks(request):
    ordering = request.GET.get('ordering')

    tasks = Task.objects.all()

    if ordering:
        tasks = tasks.order_by(ordering)

    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def create_comment(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskCommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(task=task, commenter=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_comments(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

    comments = task.comments.all()
    serializer = TaskCommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_comment(request, comment_id):
    try:
        comment = TaskComment.objects.get(id=comment_id)
    except TaskComment.DoesNotExist:
        return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskCommentSerializer(comment)
    return Response(serializer.data)


@api_view(['PUT'])
def update_comment(request, comment_id):
    try:
        comment = TaskComment.objects.get(id=comment_id)
    except TaskComment.DoesNotExist:
        return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskCommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_comment(request, comment_id):
    try:
        comment = TaskComment.objects.get(id=comment_id)
    except TaskComment.DoesNotExist:
        return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)