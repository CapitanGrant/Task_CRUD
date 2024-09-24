from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from django.urls import reverse


class TaskApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test description',
            'completed': False
        }
        self.task = Task.objects.create(**self.task_data)

    def test_task_registration(self):
        """Тест создания новой задачи"""
        response = self.client.post(reverse('task-register'), self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'Task created')

    def test_task_list(self):
        """Тест получения списка всех задач"""
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Убедиться, что одна задача создана
        self.assertEqual(response.data[0]['title'], self.task_data['title'])

    def test_task_detail(self):
        """Тест получения информации о задаче по ID"""
        response = self.client.get(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task_data['title'])

    def test_task_detail_not_found(self):
        """Тест получения задачи с несуществующим ID"""
        response = self.client.get(reverse('task-detail', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Task not found')

    def test_task_update(self):
        """Тест обновления задачи"""
        updated_data = {
            'title': 'Updated Task',
            'description': 'Updated description',
            'completed': True
        }
        response = self.client.put(reverse('task-update', args=[self.task.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Task updated')

    def test_task_delete(self):
        """Тест удаления задачи"""
        response = self.client.delete(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Task deleted')

    def test_task_delete_not_found(self):
        """Тест удаления несуществующей задачи"""
        response = self.client.delete(reverse('task-delete', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Task not found')

    def test_task_delete_all(self):
        """Тест удаления всех задач"""
        response = self.client.delete(reverse('task-delete-all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'All tasks deleted')
        self.assertEqual(Task.objects.count(), 0)  # Проверить, что все задачи удалены
