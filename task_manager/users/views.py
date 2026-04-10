from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.views import View
from . forms import RegisterUserForm, UpdateUserForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from task_manager.mixins.login import CustomLoginRequieredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = 'users'

    def get_queryset(self, *kwargs):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserCreateView(BaseCreateView):

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render (request, 'users/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Пользователь успешно зарегистрирован')
            return redirect('login')    
        return render (request, 'users/create_form.html', {'form': form})


class UserFormUpdateView(CustomLoginRequieredMixin, View):
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


class UserDeleteView(CustomLoginRequieredMixin, UserPassesTestMixin, View):

     def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return self.request.user == user
     
     def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, 'У вас нет прав для изменения другого пользователя.')
        return redirect("users_list")

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
