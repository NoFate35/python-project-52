from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from task_manager.tasks.models import Task
from django.views import View
from . forms import TaskCreateForm, TaskFilterForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = 'tasks'

    def get_queryset(self, *kwargs):
        return Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TaskFilterForm()
        context['form'] = form
        return context


class TaskCreateView(BaseCreateView):

    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()
        return render (request, 'tasks/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            messages.add_message(request, messages.SUCCESS, 'Задача успешно создана')
            return redirect('tasks_list')
        return render (request, 'tasks/create_form.html', {'form': form})


class TaskFormUpdateView(View):

     def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        form = TaskCreateForm(instance=task)
        return render(request, 'tasks/create_form.html', {"form": form})
     
     def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Задача успешно изменена')
            return redirect("tasks_list")
        return render(request, "tasks/create_form.html", {"form": form})


class TaskDeleteView(View):

     def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        if task.author == request.user:
            return render(request, 'tasks/delete.html', {"task": task})
        messages.add_message(request, messages.ERROR, 'Задачу может удалить только ее автор')
        return redirect("tasks_list")
     
     def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        if task and (task.author == request.user):
            task.delete()
            messages.add_message(request, messages.SUCCESS, 'Задача успешно удалена')
        messages.add_message(request, messages.ERROR, 'Задачу может удалить только ее автор')
        return redirect("tasks_list")

class TaskShowView(View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs["pk"])
        return render(request, "tasks/show.html", context={"task": task})
