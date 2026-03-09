from task_manager.statuses.models import Status
from django import forms



class StatusCreateForm(forms.ModelForm):

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
        elif self.instance.pk:
            self.fields['name'].widget.attrs.update({'class':"form-control is-valid"})