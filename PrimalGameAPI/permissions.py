from rest_framework.permissions import BasePermission

class IsResearcherOrSuperuser(BasePermission):
    """
    Custom permission to only allow managers and superusers to access.
    """

    def has_permission(self, request, view):
        # Check if the user belongs to the "Researcher" group or is a superuser
        return request.user.groups.filter(name='Researcher').exists() or request.user.is_superuser
    
    
    
class IsRPiClient(BasePermission):
    """
    Custom permission to only allow RPiClient to access.
    """
    def has_permission(self, request, view):
        # Check if the user belongs to the "RPiClient" group 
        return request.user.groups.filter(name='RPiClient').exists() 