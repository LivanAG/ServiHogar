from django.db import models
from django.conf import settings
from Login.models import *
# Create your models here.


class Profesional(models.Model):
    
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    Trabajos_realizados =models.IntegerField()
    valoracion = models.FloatField(default=0,blank=True,null=True)
    
    def __str__(self):
        return self.user.first_name + self.user.last_name 