from django.db import models

# Create your models here.
class RPiBoards(models.Model):
    ip_address = models.GenericIPAddressField(protocol='IPv4')  # 'both' allows both IPv4 and IPv6 addresses
    ssid = models.CharField(max_length=32 , blank=True , null=True)  # SSID lengths can vary but typically limited to 32 characters
    ssid_password = models.CharField(max_length=255, blank=True , null=True)  
    

class RPiStates(models.Model):
    rpiboard = models.OneToOneField(RPiBoards, on_delete=models.CASCADE)
    is_occupied =  models.BooleanField(default=False)
    
class LoginLogoutHist(models.Model):
    login_hist = models.DateTimeField()
    logout_hist = models.DateTimeField(blank=True , null=True)
    
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
    login_hist = models.OneToOneField(LoginLogoutHist, on_delete=models.PROTECT)
    primal = models.ForeignKey(Primals, on_delete=models.PROTECT , related_name="primal")
    