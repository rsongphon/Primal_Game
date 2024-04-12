from django.urls import path 
from . import views 

urlpatterns = [ 
    path('primals', views.PrimalsView.as_view()), 
] 