from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from task_manager.statuses.models import Status
from django.views import View
from . forms import RegisterStatusForm, UpdateStatusForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError


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
        form = RegisterStatusForm()
        return render (request, 'statuses/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = RegisterStatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Статут успешно создан')
            return redirect('statuses_list')    
        return render (request, 'statuses/create_form.html', {'form': form})

'''
class UserFormUpdateView(View):

     def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        form = UpdateUserForm(instance=user)
        return render(request, 'users/create_form.html', {"form": form})
     
     def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        form = UpdateUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Пользователь успешно изменен')
            return redirect("users_list")
        return render(request, "users/create_form.html", {"form": form})

class UserDeleteView(View):

     def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        return render(request, 'users/delete.html', {"user": user})
     
     def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs["pk"])
        if user:
            try:
                user.delete()
                messages.add_message(request, messages.SUCCESS, 'Пользователь успешно удален')
            except ProtectedError:
                messages.add_message(request, messages.ERROR, 'Невозможно удалить пользователя, потому что он используется')
            return redirect("users_list")
'''