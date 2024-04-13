from django.urls import path 
from . import views 

urlpatterns = [ 
    path('primals', views.PrimalsView.as_view()), 
    path('primals/<int:pk>', views.SinglePrimalView.as_view()), 
    path('groups/researcher/users', views.ResercherGroupManangeView.as_view()),
    path('groups/researcher/users/<int:pk>', views.ResercherDeleteView.as_view()),
    
] 