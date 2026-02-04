from django.db import models
from task_manager.statuses.models import Status
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="authors")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, related_name="executors")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name