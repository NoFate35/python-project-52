from task_manager.labels.models import Label
from django import forms



class LabelCreateForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': "Имя",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'maxlength':"100",
                                                 'class':"form-control", 
                                                 'placeholder':"Имя",
                                                 'required':""
                                                 })

        if self.errors:
            self.fields['name'].widget.attrs.update({'class':"form-control is-invalid"})
        if self.instance.pk:
            self.fields['name'].widget.attrs.update({'class':"form-control is-valid"})