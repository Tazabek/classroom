from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
from apps.cources.models import Cources
from django.urls import reverse


User = get_user_model()


class Themes(models.Model):
    name = models.CharField(max_length=155, unique=True)
    cource = models.ForeignKey(Cources, on_delete=models.CASCADE, related_name='theme')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = 'Themes'


class Tasks(models.Model):
    name = models.CharField(max_length=155)
    instruction = models.TextField()
    file = models.FileField(upload_to='tasks/', blank=True, null=True)
    points = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_checked = models.BooleanField(default=False)
    is_missed = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)
    theme = models.ForeignKey(Themes, on_delete=models.SET_NULL, blank=True, null=True, related_name='task')
    cource = models.ForeignKey(Cources, on_delete=models.CASCADE, related_name='task')
    added_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)


    def get_task_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})
    
    def task_points_url(self):
        return reverse('task-points', kwargs={'pk': self.pk})
    
    def add_file(self):
        return reverse('add-file', kwargs={'pk': self.pk})
    
    def change_task(self):
        return reverse('change-task', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.name
    
    
    class Meta:
        verbose_name_plural = 'Tasks'


class Comments(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='comment')

    def __str__(self) -> str:
        return self.text


class Points(models.Model):
    points = models.IntegerField()
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='point')

    def update_point(self):
        return reverse('update-point', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.student.username
    

class Files(models.Model):
    file = models.FileField(upload_to='task-files/')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)

    def update_file(self):
        return reverse('change-file', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.student.username
    

