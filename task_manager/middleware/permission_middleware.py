from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages


class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        #если в имени запрашиваемой view есть Update либо Delete то проверка дальше
        if ("UpdateView" in str(view_func.__dict__)) or ("DeleteView" in str(view_func.__dict__)) or ("StatusCreateView" in str(view_func.__dict__)):
            #если пользователь не залогинен
            if not request.user.is_authenticated:
                messages.add_message(request, messages.ERROR, 'Вы не авторизованы! Пожалуйста, выполните вход.')
                return redirect("login")
            # если пользователь залогинен
            else:
                #если в имени запрашиваемой view есть UserUpdate либо UserDelete то проверка дальше
                if ("UserFormUpdateView" in str(view_func.__dict__)) or ("UserDeleteView" in str(view_func.__dict__)):
                    user = get_object_or_404(User, pk=view_kwargs["pk"])
                    #сравнение пользователя из сессии с запрашиваемым
                    if request.user != user:
                        messages.add_message(request, messages.ERROR, 'У вас нет прав для изменения другого пользователя.')
                        return redirect("users_list")