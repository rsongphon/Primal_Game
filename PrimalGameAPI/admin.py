from django.contrib import admin
from .models import RPiBoards, RPiStates,Primals, Games, GameInstances

# Register your models here.
admin.site.register(RPiBoards)
admin.site.register(RPiStates)
admin.site.register(Primals)
admin.site.register(Games)
admin.site.register(GameInstances)

