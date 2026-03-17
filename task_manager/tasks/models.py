from django.db import models
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="authors")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name="executors")
    labels = models.ManyToManyField(Label, blank=True, related_name='labels')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
