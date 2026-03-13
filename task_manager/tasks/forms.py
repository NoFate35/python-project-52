from django import forms
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User
from task_manager.labels.models import Label


class TaskCreateForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label="Статус")
    executor = forms.ModelChoiceField(queryset=User.objects.all(), label="Исполнитель")
    labels = forms.ModelMultipleChoiceField(queryset=Label.objects.all(), widget=forms.SelectMultiple, label="Метки")
    

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {'name': "Имя",
                  'author': 'Автор'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
                                                 'class':"form-control", 
                                                 'placeholder':"Имя",
                                                 })
        self.fields['description'].widget.attrs.update({'class':"form-control", 
                                                        'placeholder':"Описание",
                                                        })
        self.fields['status'].widget.attrs.update({'class':"form-select"})
        self.fields['executor'].widget.attrs.update({'class':"form-select"})
        self.fields['labels'].widget.attrs.update({'class':"form-select"})