from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User




class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

class UpdateUserForm(RegisterUserForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
    
    def clean_username(self):
        usernames = User.objects.only("username")
        print('uuusernames', self.cleaned_data)
        username = self.cleaned_data['username']
        return username