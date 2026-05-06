from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User


class CustomUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        return self.request.user == user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.add_message(
                self.request,
                messages.ERROR,
                "Вы не авторизованы! Пожалуйста, выполните вход.",
            )
            return redirect("login")
        messages.add_message(
            self.request,
            messages.ERROR,
            "У вас нет прав для изменения другого пользователя.",
        )
        return redirect("users_list")
