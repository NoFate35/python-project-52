from django import forms
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
#from task_manager.labels.models import Label


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Статус")
    executor = forms.ModelChoiceField(queryset=User.objects.all(), label="Исполнитель")
    #labels = forms.MultipleChoiceField(queryset=Label.objects.all(), label="Метки")
    

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']