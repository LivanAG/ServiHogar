from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import uuid
# Create your models here.

class Provincia(models.Model):
    nombre = models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.nombre


class Municipio(models.Model):
    provincia = models.ForeignKey(Provincia,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.nombre
        


class User(User):
    class Meta:
        permissions = [
            ('Carpinteria', 'Carpinteria'),
            ('Pintura', 'Pintura'),
            ('Electricidad', 'Electricidad'),
            ('Herreria', 'Herreria'),
            ('Limpieza', 'Limpieza'),
            ('Plomeria', 'Plomeria'),
            ('Jardineria', 'Jardineria'),
            ]
    token = models.UUIDField(primary_key=False,editable=False,blank=True,null=True)        
    CantidadDeTrabajosConNosotros=models.IntegerField(default=0)
    telefono=models.CharField(max_length=8,blank=True,null=True)
    callePrincipal=models.CharField(max_length=20)
    entreCalle1=models.CharField(max_length=20)
    entreCalle2=models.CharField(max_length=20)
    numeroDeLaCasa= models.IntegerField()
    provincia = models.ForeignKey(Provincia,on_delete=models.CASCADE)
    municipio = models.ForeignKey(Municipio,on_delete=models.CASCADE)
    direccion = models.CharField(max_length=100,blank=True,null=True)
    valoracion = models.FloatField(default=0,blank=True,null=True)
    #resegna = models.CharField(default=None, max_length=250,blank=True,null=True)
    REQUIRED_FIELDS = ['callePrincipal', 'entreCalle1','entreCalle2','numeroDeLaCasa',"first_name"]

    

    def save(self,*args,**kwargs):
        if self.pk is None:
            self.direccion="{0},{1}, Calle {2} / Calle {3} y Calle {4} No {5}".format(self.provincia,self.municipio,self.callePrincipal,self.entreCalle1,self.entreCalle2,self.numeroDeLaCasa)
        super().save(*args,**kwargs)


class Notificacion(models.Model):
    
    token = models.UUIDField(primary_key=True,editable=False)  
    
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    categoria = models.CharField(max_length=50)
    titulo = models.CharField(max_length=50)
    mensaje = models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        if self.pk is None:
            self.token = uuid.uuid4()
        super().save(*args,**kwargs)


class Trabajador(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cargo=models.CharField(max_length=50,blank=True,null=True)      
    linkFaceBook=models.CharField(max_length=50,blank=True,null=True)
    linkTwitter=models.CharField(max_length=50,blank=True,null=True)
    linkIG=models.CharField(max_length=50,blank=True,null=True)
    linkLinkedin=models.CharField(max_length=50,blank=True,null=True)
    imagen = models.ImageField(upload_to='Imagenes de Perfil de Trabajadores',blank=True,null=True)
    def __str__(self):
        return self.user.first_name +" "+ self.user.last_name 



