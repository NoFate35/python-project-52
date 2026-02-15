from django.test import TestCase
from task_manager.tasks.models import Task
from django.contrib.auth.models import User


class TasksTest(TestCase):
    fixtures = ["tasks.json", "users.json", "statuses.json"]

    def setUp(self):
        self.task1 = Task.objects.get(name='task1')
        self.tasks = Task.objects.all()
    
    def test_fixtures(self):
        #проверка статуса по названию, запрос из базы
        self.assertEqual(self.task1.name, "task1")
        #по общему количеству, запрос из базы
        self.assertEqual(len(self.tasks), 1)
