from django.test import TestCase
from task_manager.tasks.models import Task
from django.contrib.auth.models import User
from django.urls import reverse


class TasksTest(TestCase):
    fixtures = ["tasks.json", "users.json", "statuses.json"]

    def setUp(self):
        self.list_url = self.list_url = reverse("tasks_list")
        self.task1 = Task.objects.get(name='task1')
        self.tasks = Task.objects.all()
    
    def test_fixtures(self):
        #проверка статуса по названию, запрос из базы
        self.assertEqual(self.task1.name, "task1")
        #по общему количеству, запрос из базы
        self.assertEqual(len(self.tasks), 2)
    
    def test_tasks_list(self):
        #отображение списка пользователей
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задачи')

        #по общему количеству
        self.assertIn("tasks", response.context)
        tasks = response.context["tasks"]
        self.assertTrue(len(tasks) == 2)
    
