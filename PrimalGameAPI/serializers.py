from rest_framework import serializers
from .models import RPiBoards, RPiStates, LoginLogoutHist, Primals, Games, GameInstances
from django.contrib.auth.models import User , Group

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ['name',]

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'username','first_name','last_name','email','date_joined','groups']
        
class UserNamePOSTSerializer(serializers.Serializer):
    username = serializers.CharField()

class PrimalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Primals
        fields = ['id','name']
        
        