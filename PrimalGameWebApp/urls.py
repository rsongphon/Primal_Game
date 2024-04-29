from django.urls import path , include
from . import views
from django.contrib.auth import views as authviews

app_name = 'webapp'

urlpatterns = [
    path("", views.home, name="home"),
    path("register-primals/", views.primals, name="register-primals"),
    path("start-game/", views.start_game, name="start-game"),
]