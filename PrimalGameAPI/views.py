from django.shortcuts import render
from rest_framework import generics
from .models import Primals , RPiBoards , RPiStates , Games , GameInstances
from .permissions import IsResearcherOrSuperuser , IsRPiClient
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from .serializers import PrimalsSerializer , UserSerializer , UserNamePOSTSerializer , RPiBoardsSerializer , RPiStatesSerializer , GamesSerializer , GamesInstancesSerializer

# Create your views here.

# Primals views
class PrimalsView(generics.ListCreateAPIView):
    queryset = Primals.objects.all()
    serializer_class = PrimalsSerializer
    # Define permission classes for different methods
    def get_permissions(self):
        if self.request.method == 'GET':
            # Return permission classes for GET request
            return [AllowAny()]
        elif self.request.method == 'POST':
            # Return permission classes for POST request
            return [IsAuthenticated(), IsResearcherOrSuperuser()]
        return super().get_permissions()

class SinglePrimalView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Primals.objects.all()
    serializer_class = PrimalsSerializer
    # Define permission classes for different methods
    def get_permissions(self):
        if self.request.method == 'GET':
            # Return permission classes for GET request
            return [AllowAny()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            # Return permission classes for POST request
            return [IsAuthenticated(), IsResearcherOrSuperuser()]
        return super().get_permissions()
    
    
# RPi views

class RPiBoradsView(generics.ListCreateAPIView):
    queryset = RPiBoards.objects.all()
    serializer_class = RPiBoardsSerializer
    # Define permission classes for different methods
    def get_permissions(self):
        if self.request.method == 'GET':
            # Return permission classes for GET request
            return [AllowAny()]
        elif self.request.method == 'POST':
            # Return permission classes for POST request
            return [IsAuthenticated(), IsResearcherOrSuperuser()]
        return super().get_permissions()

class SingleRPiBoardView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RPiBoards.objects.all()
    serializer_class = RPiBoardsSerializer
    # Define permission classes for different methods
    def get_permissions(self):
        if self.request.method == 'GET':
            # Return permission classes for GET request
            return [AllowAny()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH' or self.request.method == 'DELETE':
            # Return permission classes for POST request
            return [IsAuthenticated(), IsResearcherOrSuperuser() , IsRPiClient()]
        return super().get_permissions()
    
class RPiStatesView(generics.ListCreateAPIView):
    queryset = RPiStates.objects.all()
    serializer_class = RPiStatesSerializer
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser]
    
class SingleRPiStateViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = RPiStates.objects.all()
    serializer_class = RPiStatesSerializer
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser, IsRPiClient]
    
class GamesView(generics.ListCreateAPIView):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser]

class SingleGameView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser]
    
class GameInstancesView(generics.ListCreateAPIView):
    queryset = GameInstances.objects.all()
    serializer_class = GamesInstancesSerializer
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser]

class SingleGameInstanceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameInstances.objects.all()
    serializer_class = GamesInstancesSerializer
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser, IsRPiClient]
    
    


##### Group management views

class ResercherGroupManangeView(generics.ListCreateAPIView):
    #  filter by "Researcher" group.
    researcher_group = Group.objects.get(name='Researcher')
    queryset = User.objects.filter(groups=researcher_group)
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser]
    
    # override get_serializer_class to define each serailizer in each Method
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserNamePOSTSerializer

    # overide post method
    def post(self, request):
        # deserialization
        serialize_item = self.get_serializer(data=request.data)
        serialize_item.is_valid(raise_exception=True)
        username = serialize_item.validated_data['username']
        try:
            # assign user to manager grouop
            user = User.objects.get(username=username)
            researcher_group = Group.objects.get(name='Researcher')
            user.groups.add(researcher_group)
            return Response({'message': f'{user.username} added to group {researcher_group.name}'}, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    

class ResercherDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsResearcherOrSuperuser]
    
    def delete(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
            researcher_group = Group.objects.get(name='Researcher')
						# if user does not in Researcher group -> Raise 400_BAD_REQUEST
						# Othwise delete user from group -> retrun 200
            if researcher_group in user.groups.all():
                user.groups.remove(researcher_group)
                return Response({'message': f'{user.username} removed from group {researcher_group.name}'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is not in the specified group'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
