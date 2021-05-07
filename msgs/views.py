from django.shortcuts import render

# Create your views here.
from .serializers import MessageSerializer
from .models import Message
from msgs.models import Message
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status


class MessageSerializer(viewsets.ModelViewSet):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

