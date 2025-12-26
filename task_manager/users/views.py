from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import BaseCreateView
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.views import View
from . forms import RegisterForm


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
        form = RegisterForm()
        return render (request, 'users/create_form.html', {'form': form})


    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')    
        return render (request, 'users/create_form.html', {'form': form})

class UserFormUpdateView(View):
     def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["id"])
        form = RegisterForm(instance=user)
        return render(
            request, 'users/create_form.html', {"form": form} )
     def post(self, request, *args, **kwargs):
         article = get_object_or_404(Article, id=kwargs["id"])
         form = ArticleForm(request.POST, instance=article)
         if form.is_valid():
             form.save()
             return redirect("article_list")
         return render(request, "articles/form.html", {"form": form})
