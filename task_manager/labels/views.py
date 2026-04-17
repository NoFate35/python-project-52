from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from task_manager.labels.models import Label
from django.views import View
from . forms import LabelCreateForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from task_manager.mixins.login import CustomLoginRequieredMixin


class LabelListView(CustomLoginRequieredMixin, ListView):
    model = Label
    template_name = "labels/label_list.html"
    context_object_name = 'labels'

    def get_queryset(self, *kwargs):
        return Label.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LabelCreateView(CustomLoginRequieredMixin, BaseCreateView):

    def get(self, request, *args, **kwargs):
        form = LabelCreateForm()
        return render (request, 'labels/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = LabelCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Метка успешно создана')
            return redirect('labels_list')
        return render (request, 'labels/create_form.html', {'form': form})


class LabelFormUpdateView(CustomLoginRequieredMixin, View):

     def get(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs["pk"])
        form = LabelCreateForm(instance=label)
        return render(request, 'labels/create_form.html', {"form": form})
     
     def post(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs["pk"])
        form = LabelCreateForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Метка успешно изменена')
            return redirect("labels_list")
        return render(request, "labels/create_form.html", {"form": form})


class LabelDeleteView(CustomLoginRequieredMixin, View):

     def get(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs["pk"])
        return render(request, 'labels/delete.html', {"label": label})
     
     def post(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=kwargs["pk"])
        if label.task_set.all().count() > 0:
            messages.add_message(request, messages.ERROR, 'Невозможно удалить метку, потому что она используется')
        else:
            label.delete()
            messages.add_message(request, messages.SUCCESS, 'Метка успешно удалена')
        return redirect("labels_list")