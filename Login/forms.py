from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth.forms import SetPasswordForm

class LoginForm (AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'
            i.field.widget.attrs['placeholder'] = i.name
            i.field.widget.attrs['autocomplete'] = 'off' 


class FormRegistro(UserCreationForm):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'


    first_name=forms.CharField(
        max_length=30,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'})
        )
        
    last_name=forms.CharField(
        max_length=30,
        min_length=2,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Apellido'})
        )

 
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all() ,widget=forms.Select(attrs={'placeholder':"Provincia"}))

    municipio = forms.ModelChoiceField(queryset=Municipio.objects.all())


    class Meta:
        model=User
                
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'callePrincipal',
            'entreCalle1',
            'entreCalle2',
            'numeroDeLaCasa',
            'provincia',
            'municipio',
            'direccion',
        )
        widgets={
           
            
            'username': forms.TextInput(attrs={
                'placeholder':'Usuario',
                'autocomplete':'off'}),
            
            'email': forms.EmailInput(attrs={
                'placeholder':'Correo Electronico',
                'autocomplete':'off'}),            
            

            'callePrincipal': forms.TextInput(attrs={
                'placeholder':'Calle Principal',
                'autocomplete':'off'}),

            'entreCalle1': forms.TextInput(attrs={
                'placeholder':'Entre Calle 1',
                'autocomplete':'off'}),

            'entreCalle2': forms.TextInput(attrs={
                'placeholder':'Entre Calle 2',
                'autocomplete':'off'}),

            'numeroDeLaCasa': forms.NumberInput(attrs={
                'placeholder':'Numero',
                'autocomplete':'off'}),
        }

        error_messages={
        
            'username':{
                'unique': "Ya existe una cuenta con este nombre de usuario",
                'required': "Tiene que escribir un usuario",
                'max_length': "Usuario demasiado largo",
                'min_length': "Usuario demasiado corto",  
                },

            'email':{

                'required': "Debe escribir un correo",
                'invalid': "Direccion de correo no valida",  
                },

            'callePrincipal':{
                'required': "Tiene que escribir una Calle Principal",
                'max_length': "Nombre de Calle demasiado largo",
                'min_length': "Nombre de Calle demasiado corto",  
                },
            
            'entreCalle1':{
                'required': "Tiene que escribir una EntreCalle",
                'max_length': "Nombre de EntreCalle1 demasiado largo",
                'min_length': "Nombre de EntreCalle1 demasiado corto",  
                },
            
            'entreCalle2':{
                'required': "Tiene que escribir una EntreCalle2",
                'max_length': "Nombre de EntreCalle2 demasiado largo",
                'min_length': "Nombre de EntreCalle2 demasiado corto",  
                },
           
        }
       

class PassReset1Form(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Introduzca su direccion de Correo'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists() == False:
            self.add_error('email','Este email no existe')

    def get_user(self):
        email = self.cleaned_data.get('email')
        return User.objects.get(email=email)


class PassReset2Form(SetPasswordForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i in self.visible_fields():
            i.field.widget.attrs['class'] = 'form-control'
            i.field.widget.attrs['autocomplete'] = 'off' 
       
        self.fields['new_password1'].widget.attrs.update({'placeholder': 'Nueva Contraseña'})
        self.fields['new_password2'].widget.attrs.update({'placeholder': 'Confirme Contraseña'})
