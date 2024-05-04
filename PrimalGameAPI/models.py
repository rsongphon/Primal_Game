from django.db import models

# Create your models here.
class RPiBoards(models.Model):
    board_name = models.CharField(max_length=255, default="")  # used to indicated board rather that id
    ip_address = models.GenericIPAddressField(protocol='IPv4')  # 'both' allows both IPv4 and IPv6 addresses
    ssid = models.CharField(max_length=32 , blank=True , null=True)  # SSID lengths can vary but typically limited to 32 characters
    ssid_password = models.CharField(max_length=255, blank=True , null=True)  
    def __str__(self)-> str:
	    return self.board_name
    

class RPiStates(models.Model):
    rpiboard = models.OneToOneField(RPiBoards, on_delete=models.CASCADE)
    is_occupied =  models.BooleanField(default=False)
    start_game =  models.BooleanField(default=False)
    gp17 = models.BooleanField(default=False)
    def __str__(self)-> str:
	    return self.rpiboard.board_name
 
class Primals(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self)-> str:
	    return self.name
    
    
class Games(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self)-> str:
	    return self.name

class GameInstances(models.Model):
    game = models.ForeignKey(Games, on_delete=models.PROTECT)
    rpiboard = models.ForeignKey(RPiBoards, on_delete=models.PROTECT , related_name="rpiboard")
    primal = models.ForeignKey(Primals, on_delete=models.PROTECT , related_name="primal")
    login_hist = models.DateTimeField()
    logout_hist = models.DateTimeField(blank=True , null=True)