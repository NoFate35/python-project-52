from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=200, 
                            unique=True, 
                            error_messages={"unique": "Task status с таким Имя уже существует."})
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    #modified_at = models.DateTimeField(auto_now_add=True, null=True)
