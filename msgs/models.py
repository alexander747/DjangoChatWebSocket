from django.db import models
from users.models import User
from room.models import Room


class Message(models.Model):
    image = models.ImageField(upload_to='assets/upload', blank=True, null=True)
    mensaje = models.CharField( 'Mensaje', max_length=500 )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)