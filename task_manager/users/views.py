from django.shortcuts import render, redirect
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from . forms import RegisterForm


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    query_string = User.objects.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class UserFormView(BaseCreateView):

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render (request, 'auth/user_create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password == password2:
                form.save()
            return redirect('user_list')