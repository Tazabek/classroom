from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True)

    def room_url(self):
        return reverse('private-room', kwargs={'pk': self.pk})
    
    def teacher_room_url(self):
        return reverse('private-with-teacher', kwargs={'pk': self.pk})


    def __str__(self) -> str:
        return self.username
    