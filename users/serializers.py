from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password']

    def create(self, validated_data):
        print(validated_data)
        user = User(**validated_data)
        user.set_password( validated_data['password'] )    
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)  
        updated_user.set_password( validated_data['password'] )  
        updated_user.save()
        return updated_user

class UserSerializerToken(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email') 