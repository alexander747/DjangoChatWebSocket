from django.shortcuts import render

# Create your views here.
from .serializers import UserSerializer, UserSerializerToken
from .models import User
from msgs.models import Message
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
#para login
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
#para cerrar login
from rest_framework.views import APIView
#para login sesiones
from django.contrib.sessions.models import Session
from datetime import datetime
#para token
from users.authentication_mixins import Authentication

class UserSerializerClass( viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class( data = request.data, context={'request':request} )
        if login_serializer.is_valid():
            print(login_serializer.validated_data['user'])
            user = login_serializer.validated_data['user']
            #validamos si esta activo
            if user.is_active:
                token, created = Token.objects.get_or_create( user=user )
                user_serializer = UserSerializerToken( user )
                if created:
                    return Response( {'ok':True, 'token':token.key, 'user':user_serializer.data}, status = status.HTTP_201_CREATED)
                else:
                    #si inicia sesion cierra sesiones por el nuevo token
                    all_sessions = Session.objects.filter( expire_date__gte = datetime.now() )
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int( session_data.get('_auth_user_id') ):
                                session.delete()
                    #actualiza el token si vuelve a iniciar sesion
                    token.delete()    
                    token = Token.objects.create(user=user)
                    return Response( {'ok':True, 'token':token.key, 'user':user_serializer.data}, status = status.HTTP_201_CREATED)
            else:
                return Response({'ok':False, 'error':'Usuario no activo'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'ok':False, 'error':'Credenciales incorrectas'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'ok':False, 'message':'Hola desde response'}, status = status.HTTP_200_OK)


class Logout(APIView):
    def get(self, request, *args, **kwargs):
        try:
            token = request.GET.get('token') #desde el front end envia la variable token por get
            token = Token.objects.filter( key=token ).first()
            if token:
                user = token.user
                all_sessions = Session.objects.filter( expire_date__gte = datetime.now() )
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int( session_data.get('_auth_user_id') ):
                            session.delete()

                token.delete()
                token_message = 'Token eliminado'  
                return Response({'ok':True, 'Token_message':token_message}, status = status.HTTP_200_OK)       

            return Response({'ok':False, 'message':'No se ha encontrado una sesion con este token'}, status = status.HTTP_400_BAD_REQUEST)              

        except:
            return Response({'ok':False, 'message':'No se ha encontrado token en la peticion'}, status = status.HTTP_409_CONFLICT)              
             

class RefrescarToken(APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        print(username)
        try:
            user_token = Token.objects.get(
                user=UserSerializerToken().Meta.model.objects.filter(username=username).first()
            )
            print(user_token)
            return Response({'token':user_token.key})
        except:
            return Response({'error':'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)    