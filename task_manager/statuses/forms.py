from task_manager.statuses.models import Status
from django import forms



class RegisterStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']

class UpdateStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']
    
    def clean_username(self):
        name = self.cleaned_data['name']
        return name