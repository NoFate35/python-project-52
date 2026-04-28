from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from task_manager.tasks.models import Task
from django.views import View
from .forms import TaskCreateForm, TaskFilterForm
from django.contrib import messages
from task_manager.mixins.login import CustomLoginRequieredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class TaskListView(CustomLoginRequieredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self, *kwargs):
        form = TaskFilterForm(self.request.GET)
        tasks = Task.objects.all()
        if form.is_valid():
            query = dict()
            if form.cleaned_data.pop("self_author"):
                query["author"] = self.request.user
            query.update(
                {
                    key: value
                    for key, value in form.cleaned_data.items()
                    if value is not None
                }
            )
            tasks = tasks.filter(**query)
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TaskFilterForm()
        context["form"] = form
        return context


class TaskCreateView(CustomLoginRequieredMixin, BaseCreateView):
    def get(self, request, *args, **kwargs):
        form = TaskCreateForm()
        return render(request, "tasks/create_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            task.labels.set(form.cleaned_data["labels"])
            messages.add_message(request, messages.SUCCESS, "Задача успешно создана")
            return redirect("tasks_list")
        return render(request, "tasks/create_form.html", {"form": form})


class TaskFormUpdateView(CustomLoginRequieredMixin, View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        form = TaskCreateForm(instance=task)
        return render(request, "tasks/create_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        form = TaskCreateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            task.labels.set(form.cleaned_data["labels"])
            messages.add_message(request, messages.SUCCESS, "Задача успешно изменена")
            return redirect("tasks_list")
        return render(request, "tasks/create_form.html", {"form": form})


class TaskDeleteView(CustomLoginRequieredMixin, UserPassesTestMixin, View):
    def test_func(self):
        task = get_object_or_404(Task, pk=self.kwargs["pk"])
        return task.author == self.request.user

    def handle_no_permission(self):
        messages.add_message(
            self.request, messages.ERROR, "Задачу может удалить только ее автор"
        )
        return redirect("tasks_list")

    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        return render(request, "tasks/delete.html", {"task": task})

    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs["pk"])
        task.delete()
        messages.add_message(request, messages.SUCCESS, "Задача успешно удалена")
        return redirect("tasks_list")


class TaskShowView(CustomLoginRequieredMixin, View):
    def get(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs["pk"])
        # print('task', task.labels.all())
        return render(request, "tasks/show.html", context={"task": task})
