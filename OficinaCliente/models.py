from django.db import models
from Login.models import *
from Profesional.models import Profesional
from django.forms import model_to_dict
# Create your models here.


class Servicio(models.Model):
    Titulo = models.CharField(max_length=30)
    Imagen=models.ImageField(upload_to='Servicios')
    Icono = models.CharField(max_length=50,default='')
    Descripcion = models.CharField(max_length=200,default='')
    def __str__(self):
        return self.Titulo

    def toJSON(self):
        return model_to_dict(self)

        
class Orden(models.Model):
    tipoDeServicio = models.ForeignKey(Servicio,on_delete=models.CASCADE)
    cliente=models.ForeignKey(User,on_delete=models.CASCADE)
    profesional=models.ForeignKey(Profesional,on_delete=models.CASCADE,blank=True,null=True)
    estado = models.CharField(max_length=20)
    FechaDeEntrada=models.DateTimeField(auto_now_add=True)
    FechaLimite=models.DateTimeField()
    cliente_TrabajoTerminado = models.BooleanField(default=False)
    profesional_TrabajoTerminado = models.BooleanField(default=False)
    valoracion_Cliente=models.FloatField(default=0,blank=True,null=True)
    valoracion_Profesional=models.FloatField(default=0,blank=True,null=True)
    resegna_Cliente = models.CharField(max_length=150,default="",blank=True,null=True)
    resegna_Profesional = models.CharField(max_length=150,default="",blank=True,null=True)
    confirmacion_de_pago=models.BooleanField(default=True)
	
    def toJSON(self):
        return model_to_dict(self)

class ResegnaEmpresa(models.Model):
    
    usuario=models.OneToOneField(User,on_delete=models.CASCADE)
    mensaje = models.CharField(default=None, max_length=250,blank=True,null=True)
    valoracion = models.FloatField(default=0,blank=True,null=True)

    class Meta:
        ordering = ["-valoracion"]

