from django.contrib.auth.mixins import UserPassesTestMixin

class CustomUserPassesTestMixin(UserPassesTestMixin):
    permission_denied_message = 'У вас нет прав для изменения другого пользователя.'