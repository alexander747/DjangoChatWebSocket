from django.shortcuts import render

# Create your views here.
from .serializers import RoomSerializer
from .models import Room
from msgs.models import Message
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # @action(methods=['GET'], detail=True)
    # def messages(self, request, pk=None):
    #     room = self.get_object()

    #     messages = Message.objects.filter(room=int(room.id))
    #     serialized = MessageSerializer(messages, many=True)
    #     return Response(status=status.HTTP_200_OK, data=serialized.data)