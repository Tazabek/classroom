from django import forms
from apps.tasks.models import Tasks, Points, Files


class ChangeTaskForms(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'instruction', 'file', 'points', 'deadline', 'theme']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TaskForms(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['file', 'deadline', 'points']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'deadline' : forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'})
        }


class PointForm(forms.ModelForm):
    class Meta:
        model = Points
        fields = ['points']


class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ['file']
        