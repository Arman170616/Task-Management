from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task

class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create a sample task
        self.task = Task.objects.create(
            task_name='Sample Task',
            description='This is a sample task',
            due_date='2023-07-31',
            assignee=self.user
        )

    def test_create_task(self):
        url = reverse('create-task')
        data = {
            'task_name': 'New Task',
            'description': 'This is a new task',
            'due_date': '2023-08-15',
            'assignee': self.user.id
        }
        self.client.force_authenticate(user=self.user)  # Authenticate the test client
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

        # Verify the created task's attributes
        task = Task.objects.last()
        self.assertEqual(task.task_name, 'New Task')
        self.assertEqual(task.description, 'This is a new task')
        self.assertEqual(task.due_date.strftime('%Y-%m-%d'), '2023-08-15')
        self.assertEqual(task.assignee, self.user)

    def test_get_task(self):
        url = reverse('get-task', args=[self.task.id])
        self.client.force_authenticate(user=self.user)  # Authenticate the test client
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)






