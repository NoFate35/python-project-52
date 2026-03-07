from django import forms
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Статус")
    executor = forms.ModelChoiceField(queryset=User.objects.all(), label="Исполнитель")

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']