from django import forms
from django.contrib.auth.models import User

from . import models

class ReportCreateForm(forms.ModelForm):
  class Meta:
    model = models.Entries
    fields = ['date', 'distance', 'duration']
    widgets = {
            'date': forms.DateTimeInput(format=('%d/%m/%Y %H:%M'), 
                                             attrs={'type':'datetime-local', 'style':'width:220px'}),
            'distance': forms.NumberInput(attrs={'type': 'number', 'style':'width:220px'}),
            'duration': forms.TimeInput(attrs={'type': 'text', 'step': 2, 'value':'00:15:15', 'class':'html-duration-picker', 'style':'width:95px'})
        }