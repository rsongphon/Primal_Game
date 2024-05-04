from django.urls import path , include
from . import views
from django.contrib.auth import views as authviews

app_name = 'webapp'

urlpatterns = [
    path("", views.home, name="home"),
    path('profile/<username>', views.profile, name='profile'),
    path("register-primals/", views.primals, name="register-primals"),
    path("start-game/", views.start_game, name="start-game"),
    path("game-page/<int:gameinstance>",views.game_push_button_page, name="game-page"),
    path("handle-signal/<int:gameinstance>",views.game_push_button_handle_signal, name="handle-signal"),
]