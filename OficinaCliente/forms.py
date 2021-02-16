from django import forms
from .models import *
from Login.models import *
from django.forms import ModelForm
from datetime import datetime,timedelta,timezone
from django.contrib.auth.views import PasswordChangeForm


class OrdenForm(ModelForm):
    class Meta:
        model = Orden
        fields = ['FechaLimite','cliente','tipoDeServicio','estado']
        
        widgets = {
            'FechaLimite': forms.DateTimeInput(
                format='%m/%d/%y %H:%M',
                attrs={},
                ),
        }
        error_messages={

         }
	
    def clean(self):
        cleaned_data = super().clean()
        msg1 = "El servicio debe ser pedido con 72 horas de antelacion"
        msg2 = "El servicio debe ser pedido en horario laboral (8 AM - 16 PM)"
        msg3 = "Ya tienes una orden de este tipo activa ( Solo puedes tener una a la vez)"
      

        """Verificando que la orden solo pueda ser pedida en horario laboral 
        y con minimo 3 dias de antelacion.
        """
        
        horarioMinimo = timedelta(hours=8)
        horarioMaximo = timedelta(hours=15)
  

        hoy = datetime.now()
        tres_dias = hoy + timedelta(days=2)

        fecha_limite = cleaned_data.get('FechaLimite')
        
        hora = timedelta(hours=fecha_limite.hour)

        #Verificando que solo pueda tener un tipo de orden activo a la vez
        orden_esta = Orden.objects.filter(cliente=cleaned_data.get('cliente'),tipoDeServicio= cleaned_data.get('tipoDeServicio'), estado__in=["Pendiente","En Proceso"])


        
        if fecha_limite<tres_dias:
            self.add_error('cliente', msg1)

           
        if  hora > horarioMaximo or hora < horarioMinimo:
            self.add_error('FechaLimite', msg2)

        if orden_esta:
            self.add_error('tipoDeServicio', msg3)
            

class CambiarPassForm(PasswordChangeForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'
            i.field.widget.attrs['autocomplete'] = 'off' 
       
        self.fields['old_password'].widget.attrs.update({'placeholder': 'Antigua Contraseña'})
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Nueva Contraseña'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirme Contraseña'})


class EditarClienteForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'


    id=forms.CharField(
        max_length=30,
        min_length=1,
        required=False,
        widget=forms.HiddenInput()
        )

    username=forms.CharField(
        max_length=30,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Usuario','class':'form-control'})
        )

    first_name=forms.CharField(
        max_length=30,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre','class':'form-control'})
        )
        
    last_name=forms.CharField(
        max_length=30,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido','class':'form-control'})
        )

    email=forms.CharField(
        max_length=30,
        min_length=2,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Correo Electronico','class':'form-control'})
        )

    callePrincipal=forms.CharField(
        max_length=50,
        min_length=1,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'CallePrincipal','class':'form-control'})
        )

    entreCalle1=forms.CharField(
        max_length=50,
        min_length=1,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Entre Calle 1','class':'form-control'})
        )

    entreCalle2=forms.CharField(
        max_length=50,
        min_length=1,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Entre Calle 2','class':'form-control'})
        )

    numeroDeLaCasa=forms.CharField(
        max_length=20,
        min_length=1,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'No','class':'form-control'})
        )

    direccion=forms.CharField(
        max_length=30,
        min_length=1,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido','class':'form-control'})
        )

    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all() ,widget=forms.Select(attrs={'placeholder':"Provincia"}))

    municipio = forms.ModelChoiceField(queryset=Municipio.objects.all())

    resegna = forms.CharField(max_length=250,min_length=10,required=False,widget=forms.Textarea(attrs={'class':"form-control my-5",'rows':'5'}))

    valoracion=forms.CharField(max_length=3,min_length=1, required=False,widget=forms.HiddenInput())

    def clean(self):
        cleaned = super().clean()
        nombreUsuario=cleaned.get('username')
        email=cleaned.get('email')
        id=cleaned.get('id')
        print(cleaned.get('id'))

        valoracion = float(cleaned.get('valoracion'))
        
        if valoracion == 0:
            self.add_error('valoracion',"Debe otorgar una Valoración!")

        if User.objects.filter(username=nombreUsuario).exclude(pk=id).exists():
            self.add_error('username','Ya existe una cuenta con este nombre de usuario')

        if User.objects.filter(email=email).exclude(pk=id).exists():
            self.add_error('email','Ya existe una cuenta con este correo electronico')
             


class ValorarForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'


    score=forms.CharField(
        max_length=3,
        min_length=1,
        required=True,
        widget=forms.HiddenInput()
        )

    id=forms.CharField(
        max_length=50,
        min_length=1,
        required=True,
        widget=forms.HiddenInput()
        )
    resegna=forms.CharField(
        max_length=200,
        min_length=2,
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Reseña (200 Caracteres)','class':'form-control','rows':'5'})
        )
    
    def clean(self):
        cleaned = super().clean()
        valoracion = float(cleaned.get('score'))
        
        if valoracion == 0:
            self.add_error('score',"Debe otorgar una Valoración!")



class ValorarEmpresaForm(forms.Form):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'


    valoracion=forms.CharField(
        max_length=3,
        min_length=1,
        required=True,
        widget=forms.HiddenInput()

        )

    mensaje=forms.CharField(
        max_length=200,
        min_length=2,
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Reseña (200 Caracteres)','class':'form-control','rows':'5'})
        )
    
    def clean(self):
        cleaned = super().clean()
        valoracion = float(cleaned.get('valoracion'))
        print("valoracion")
        print(valoracion)
        if valoracion == 0:
            self.add_error('valoracion',"Debe otorgar una Valoración!")

    
    
class CorreoForm(forms.Form):
    Asunto = forms.CharField(max_length=100,min_length=10,required=True)
    Mensaje = forms.CharField(max_length=400,min_length=10,required=True)
      
          

class ResegnaForm(forms.Form):


    Mensaje = forms.CharField(max_length=250,min_length=10,required=True,widget=forms.Textarea(attrs={'class':"form-control my-5",'rows':'5'}))