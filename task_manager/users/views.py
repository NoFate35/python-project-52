from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User

class UserListView(ListView):
    model = User
    template_name = "books/acme_list.html"
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        articles = User.objects.all().order_by("-created_at")
        return render(request, "articles/list.html", {"articles": articles,
        'query': query,})
    
class UserFormView(CreateView):
        model = User
        fields = ["username", "password"]
        template_name_suffix = '_create_form'