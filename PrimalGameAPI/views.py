from django.shortcuts import render
from rest_framework import generics
from .models import Primals
from .serializers import PrimalsSerializer


# Create your views here.
# Create your views here.
class PrimalsView(generics.ListCreateAPIView):
    queryset = Primals.objects.all()
    serializer_class = PrimalsSerializer
    
