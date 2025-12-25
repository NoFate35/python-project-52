from django.views.generic.base import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class IndexView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login_form.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    #def form_invalid(self, form):
        #return super().form_invalid(form)

    '''
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request.POST)
        print('ffform', form.cleaned_data)
        if form.is_valid():
            print('ffform', form.cleaned_data)
            form.save()
            return redirect('home')    
        return render (request, 'login_form.html', {'form': form})
    '''