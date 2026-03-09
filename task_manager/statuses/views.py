from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from task_manager.statuses.models import Status
from django.views import View
from . forms import StatusCreateForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class StatusListView(ListView):
    model = Status
    template_name = "statuses/status_list.html"
    context_object_name = 'statuses'

    def get_queryset(self, *kwargs):
        return Status.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StatusCreateView(BaseCreateView):

    def get(self, request, *args, **kwargs):
        form = StatusCreateForm()
        return render (request, 'statuses/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = StatusCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Статус успешно создан')
            return redirect('statuses_list')
        #print('fform.errors', form.errors.as_data())
        #messages.add_message(request, messages.ERROR, 'Status с таким Name уже существует.')
        return render (request, 'statuses/create_form.html', {'form': form})


class StatusFormUpdateView(View):

     def get(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs["pk"])
        form = StatusCreateForm(instance=status)
        return render(request, 'statuses/create_form.html', {"form": form})
     
     def post(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs["pk"])
        form = StatusCreateForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Статус успешно изменен')
            return redirect("statuses_list")
        messages.add_message(request, messages.ERROR, 'Status с таким Name уже существует.')  
        return render(request, "statuses/create_form.html", {"form": form})


class StatusDeleteView(View):

     def get(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs["pk"])
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