from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from task_manager.tasks.models import Task
from django.views import View
from . forms import TaskCreateForm
from django.contrib import messages


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = 'tasks'

    def get_queryset(self, *kwargs):
        return Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TaskCreateView(BaseCreateView):

    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()
        return render (request, 'tasks/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Задача успешно создана')
            return redirect('tasks_list')
        return render (request, 'tasks/create_form.html', {'form': form})


class TaskFormUpdateView(View):

     def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        form = TaskCreateForm(instance=task)
        return render(request, 'tasks/create_form.html', {"form": form})
     
     def post(self, request, *args, **kwargs):
        status = get_object_or_404(Task, pk=kwargs["pk"])
        form = TaskCreateForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Задача успешно изменена')
            return redirect("tasks_list")
        return render(request, "tasks/create_form.html", {"form": form})


class TaskDeleteView(View):

     def get(self, request, *args, **kwargs):
        status = get_object_or_404(Task, pk=kwargs["pk"])
        return render(request, 'statuses/delete.html', {"status": status})
     
     def post(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs["pk"])
        if status:
            try:
                status.delete()
                messages.add_message(request, messages.SUCCESS, 'Статус успешно удален')
            except ProtectedError:    
                messages.add_message(request, messages.ERROR, 'Невозможно удалить статус, потому что он используется')
            return redirect("statuses_list")