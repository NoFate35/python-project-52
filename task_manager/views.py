from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login_form.html'
    
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Вы залогинены')
        return reverse('home')

def logout_view(request):
    messages.add_message(request, messages.INFO, 'Вы разлогинены')
    logout(request)
    return HttpResponseRedirect(reverse('home'))
