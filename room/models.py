from django.db import models
from users.models import User


class Room(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, related_name='users')

    def __str__(self):
        return self.name