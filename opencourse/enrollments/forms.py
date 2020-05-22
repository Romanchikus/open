from . import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

class EnrollmentView(forms.ModelForm):
    
    class Meta:
        model = models.Enrollment
        fields = [
            "is_active",
        ]
        labels = {
            "is_active": _("Is active"),
        }

class HandoutForm(forms.ModelForm):
    class Meta:
        model = models.Handout
        fields = [ 'name', 'description', 'file', 'section',]
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "file": _("File"),
            "section": _("Section"),
        }
        widgets = {
            'file': forms.FileInput(attrs={'class': 'btn btn-primary'}),
        }
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('course')
    #     super(HandoutForm, self).__init__(*args, **kwargs)
        
        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['File'].widget.attrs.update({'class': 'btn btn-primary'})