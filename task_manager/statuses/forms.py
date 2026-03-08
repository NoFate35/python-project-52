from task_manager.statuses.models import Status
from django import forms



class RegisterStatusForm(forms.ModelForm):

    name = forms.CharField(label="Имя", label_suffix="")
    auto_id=True


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
                                                 'required':""
                                                 })
        if self.errors:
            self.fields['name'].widget.attrs.update({'class':"form-control is-invalid"})




class UpdateStatusForm(forms.ModelForm):

    name = forms.CharField(label="Имя", label_suffix="")

    class Meta:
        model = Status
        fields = ['name']
    
    def clean_name(self):
        name = self.cleaned_data['name']
        return name
    
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