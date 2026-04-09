from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

class CustomLoginRequieredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')