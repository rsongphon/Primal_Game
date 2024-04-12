from rest_framework import serializers
from .models import RPiBoards, RPiStates, LoginLogoutHist, Primals, Games, GameInstances

class PrimalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Primals
        fields = ['id','name']