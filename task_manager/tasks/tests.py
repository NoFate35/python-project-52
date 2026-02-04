from django.test import TestCase
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class TasksTest(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.user = User.objects.filter()
