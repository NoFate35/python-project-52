from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.views import View
from . forms import RegisterUserForm, UpdateUserForm
from django.contrib import messages


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = 'users'

    def get_queryset(self, *kwargs):
        return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserFormView(BaseCreateView):

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render (request, 'users/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')    
        return render (request, 'users/create_form.html', {'form': form})


class UserFormUpdateView(View):

     def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect("login")
        user = get_object_or_404(User, pk=kwargs["pk"])
        if request.user != user:
            messages.add_message(request, messages.ERROR, 'У вас нет прав для изменения другого пользователя.')
            return redirect("users_list")
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
