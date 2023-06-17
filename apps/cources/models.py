from typing import Iterable, Optional
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

import random
import string

User = get_user_model()


class Cources(models.Model):
    name = models.CharField(max_length=155)
    subject = models.CharField(max_length=155)
    is_archived = models.BooleanField(default=False)
    code = models.CharField(max_length=7)
    teachers = models.ManyToManyField(User, related_name='teachers')
    students = models.ManyToManyField(User, related_name='students')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    @property
    def generate_code(self):
        characters = string.ascii_lowercase + string.digits  
        code = ''.join(random.choice(characters) for _ in range(7))
        return code
    
    def save(self, *args, **kwargs):
        self.code = self.generate_code
        super().save(*args, **kwargs)


    def get_stream_url(self):
        return reverse("cource-stream", kwargs={"pk": self.pk})

    def get_tasks_url(self):
        return reverse("cource-tasks", kwargs={"pk": self.pk})
    
    def add_task_url(self):
        return reverse("add-task", kwargs={"pk": self.pk})
    
    def users_url(self):
        return reverse('users', kwargs={'pk': self.pk})
    
    def add_teacher_url(self):
        return reverse('add-teacher', kwargs={'pk': self.pk})
    
    def add_student_url(self):
        return reverse('add-student', kwargs={'pk': self.pk})
    
    def points_url(self):
        return reverse('all-points', kwargs={'pk': self.pk})
    
    def delete_cource_url(self):
        return reverse('delete-cource', kwargs={'pk': self.pk})
    
    def leave_cource(self):
        return reverse('leave-cource', kwargs={'pk': self.pk})
    
    def comming_tasks(self):
        return reverse('comming-tasks', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.name    
  
    class Meta:
        verbose_name_plural = 'Cources'



class CourceStream(models.Model):
    text = models.CharField(max_length=255)
    is_group_message = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    cource = models.ForeignKey(Cources, on_delete=models.CASCADE, related_name='stream')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream', null=True, blank=True, default=None)

    def __str__(self) -> str:
        return self.text
    
    class Meta:
        ordering = ['-id']


class StreamComments(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    stream = models.ForeignKey(CourceStream, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')

    def __str__(self) -> str:
        return self.text
    

class PrivateRoom(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')
    

    def __str__(self) -> str:
        return f'{self.student}, {self.teacher}'
    

class Messages(models.Model):
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_by')
    room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE, related_name='messages')

