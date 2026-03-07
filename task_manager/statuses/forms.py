from task_manager.statuses.models import Status
from django import forms



class RegisterStatusForm(forms.ModelForm):

    name = forms.CharField(label="Имя", label_suffix="", initial="Имя")


    class Meta:
        model = Status
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'type':"text",
                                                 'name':"name",
                                                 'maxlength':"100",
                                                 'class':"form-control", 
                                                 'placeholder':"Имя",
                                                 'required':"",
                                                 'id':"id_name"
                                                 })
   





class UpdateStatusForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']
    
    def clean_username(self):
        name = self.cleaned_data['name']
        return name