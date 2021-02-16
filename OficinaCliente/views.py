from django.shortcuts import render
import json
from django.views.generic import TemplateView,FormView,ListView,CreateView,DeleteView,DetailView
from django.utils.decorators import method_decorator
from datetime import datetime,timedelta,timezone
from django.views.decorators.csrf  import csrf_protect,csrf_exempt
from django.http import JsonResponse
from django.urls  import reverse_lazy
from .models import *
from .forms import *
from django.forms import model_to_dict
from django.core import serializers
from Login.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from email.mime.multipart import MIMEMultipart
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .consumers import RevisionConsumer
from Profesional.models import Profesional

# Create your views here.
def actualizarValoracionCliente(id):
    
    cliente = User.objects.get(pk=id)
    lista = Orden.objects.filter(estado="Finalizado",cliente_id=id)
    total = 0
    contador = 0
    for i in lista:
        if i.valoracion_Profesional!=0:
            contador+=1
            total+=i.valoracion_Profesional
        
    cliente.valoracion = total/contador
    cliente.save()

def TituloService(i_d):
    serv = Servicio.objects.get(id=i_d)
    return serv.Titulo

def enviar_mail(user,asunto,mensaje):
        try:
            # Establecemos conexion con el servidor smtp de gmail
            mailServer = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
            print(mailServer.ehlo())# Comprueba si tenemos conexion y nos da la respuesta 
            mailServer.starttls() # Establece una conexion segura
            print(mailServer.ehlo())# Comprueba si tenemos conexion y nos da la respuesta 
            mailServer.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)

            email_to=settings.EMAIL_HOST_USER
            
            # Construimos el mensaje 
            mensaje = MIMEText(mensaje)
            mensaje['From']=user.email
            mensaje['To']=email_to
            mensaje['Subject']=asunto
        
            # Envio del mensaje
            mailServer.sendmail(user.email,email_to,mensaje.as_string())

        except Exception as e:
            print(e)





class HomeView(LoginRequiredMixin,FormView):
    template_name = "OficinaCliente/home.html"
    form_class= CorreoForm

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        data={}
        usuario = request.user
        form = self.get_form()

        try:
            if form.is_valid():
                Mensaje = form.cleaned_data['Mensaje'] + "\n\nEste correo fue enviado por el usuario\nNombre: " + usuario.first_name +" "+ usuario.last_name+ "\nid: " +str(usuario.id)+ "\nEmail: " +usuario.email
  
                enviar_mail(usuario,form.cleaned_data['Asunto'],Mensaje)
            else:
                data['error']=form.errors

        except Exception as e:
            data['error']=str(e)
        
        return JsonResponse(data)


    def get_context_data(self,*args,**kwargs):
        lista_testimonios = ResegnaEmpresa.objects.filter()[:5]
        lista =[]
        for i in lista_testimonios:
            user= User.objects.get(pk = i.usuario_id)
            lista.append({'nombre':user.first_name,'apellido':user.last_name,'mensaje':i.mensaje,'valoracion':str(i.valoracion)})
              
        context= super().get_context_data(*args,**kwargs)
        context['breadcrumbs']='Home'
        context['lista_testimonios']=lista
        return context

class ServiciosView(LoginRequiredMixin,TemplateView):
    template_name = "OficinaCliente/servicios.html"
    def get_context_data(self,*args,**kwargs):
        context= super().get_context_data(*args,**kwargs)
        context['breadcrumbs']='Servicios'
        context['lista_servicios']=Servicio.objects.all()
        
        return context

class ProfesionalInfoView(LoginRequiredMixin,TemplateView):
    template_name = "OficinaCliente/profesional_info.html"

class PerfilView(LoginRequiredMixin,ListView):
    model = Orden
    template_name = "OficinaCliente/perfil.html"
    context_object_name="lista_ordenes"
    
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    
    def get(self, request ,*args, **kwargs):

        usuario = User.objects.get(pk=self.request.user.id)
       
        resegnaForm = ValorarEmpresaForm(initial={'valoracion':0})


   
        
        return render(request, self.template_name, {'breadcrumbs': 'Perfil' , 'usuario': usuario,'form':ValorarForm,'resegnaForm':resegnaForm})
    

    def post(self,request,*args,**kwargs):
        data={}
       
      
        try:

            if request.POST['action'] == 'listar':
                data=[]
             
            
                ListadoOrdenes = Orden.objects.filter(cliente_id=request.user.id,estado__in=['Pendiente','En Proceso']).values()
               
                for i in ListadoOrdenes:
     
                    i['tipoDeServicio_id'] = TituloService(i['tipoDeServicio_id']) 
                    data.append(i)

            elif request.POST['action'] == 'listarFinalizados':
                data=[]

                usuario = User.objects.get(id=self.request.user.id)
                
                for i in  Orden.objects.filter(estado="Finalizado",cliente_id=usuario.id).values():
                    profesional = Profesional.objects.get(id=i['profesional_id'])
                
                    
                    id_orden = i['id']
                    tipoDeServicio = TituloService(i['tipoDeServicio_id'])
                    FechaLimite = i['FechaLimite']
                    FechaDeEntrada = i['FechaDeEntrada']
                    estado = i['estado']
                    cliente_TrabajoTerminado = i['cliente_TrabajoTerminado']
                    
                    data.append({"id":id_orden,"tipoDeServicio":tipoDeServicio,"FechaLimite":FechaLimite,"FechaDeEntrada":FechaDeEntrada,"cliente_TrabajoTerminado":cliente_TrabajoTerminado})
                    
            elif request.POST['action'] == 'CargarDatosPerfil':
                usuario = User.objects.get(pk=self.request.user.id)
                resegna = None

                if ResegnaEmpresa.objects.filter(usuario_id = usuario.id).exists():
                    data = ResegnaEmpresa.objects.get(usuario_id = usuario.id)
                    resegna = {'valoracion':data.valoracion,'mensaje':data.mensaje}
                

                username = usuario.username
                nombre = usuario.first_name
                apellido = usuario.last_name
                email = usuario.email
                direccion = usuario.direccion
                valoracion = usuario.valoracion
                provincia = usuario.provincia
                municipio = usuario.municipio
                
                
                
                trabajosCompletados=Orden.objects.filter(estado="Finalizado",cliente_id=usuario.id).count()

                  
                data = {
                    "username":username,
                    "email":email,
                    "trabajosCompletados":trabajosCompletados,
                    "nombre":nombre,"apellido":apellido,
                    "direccion":direccion,
                    "valoracion":valoracion,
                    "provincia":provincia.nombre,
                    "municipio":municipio.nombre,
                    "resegna":json.dumps(resegna),
                    

                    }
                
            elif request.POST['action'] == 'eliminar':
                ord = Orden.objects.get(pk=request.POST['id'])
                ord.delete()
                      
            elif request.POST['action'] == 'completado':
              
               #Capturamos el profesional que ejecuto la llamada
                usuario = User.objects.get(pk=self.request.user.id)
                
                #Capturamos la orden que va a ser modificada
                orden = Orden.objects.get(id = request.POST['id'])
                

                if orden.cliente_TrabajoTerminado:
                    orden.cliente_TrabajoTerminado = False
                    orden.save()
                else:
                
                    if orden.profesional_TrabajoTerminado:
                        orden.cliente_TrabajoTerminado = True
                        orden.estado = "Finalizado"
                        orden.save()
                        usuario.CantidadDeTrabajosConNosotros=Orden.objects.filter(estado="Finalizado",cliente_id=usuario.id).count()
                        usuario.save(update_fields=['CantidadDeTrabajosConNosotros'])
                        data={"contador":usuario.CantidadDeTrabajosConNosotros}

                    
                    else:
                        orden.cliente_TrabajoTerminado = True
                        orden.save()

            elif request.POST['action'] == 'perfilProfesional':

                #Capturamos el profesional que ejecuto la llamada
                orden = Orden.objects.get(pk=request.POST['id'])
                profesional = Profesional.objects.get(pk = orden.profesional_id)
                usuario = User.objects.get(pk=profesional.user_id)
                nombre = usuario.first_name
                apellido = usuario.last_name
                cantDeTrabajosRealizados = profesional.Trabajos_realizados
          
                data= {"nombre":nombre,"apellido":apellido,"cantDeTrabajosRealizados":cantDeTrabajosRealizados}
            
            elif request.POST['action'] == 'valorarProfesional':
                from Profesional.views import actualizarValoracionProfesional

                orden = Orden.objects.get(pk=request.POST['id'])
                profesional = Profesional.objects.get(pk = orden.profesional_id)
                usuario = User.objects.get(pk=profesional.user_id)

                if request.POST['action2'] == 'cargarModal':
                    #Cargamos el modal con los datos correspondientes
                    valoracionCliente = orden.valoracion_Cliente
                    resegnaCliente = orden.resegna_Cliente
                    data= {"valoracionCliente":valoracionCliente,"resegnaCliente":resegnaCliente,'id_orden':request.POST['id'],"nombre_prof":usuario.first_name}
                
                elif request.POST['action2'] == 'salvarValoracion':
                    #Salvamos la valoracion realizada por el usuario 
                    valoracion = request.POST['score']
                    resegna = request.POST['resegna']
                    form = ValorarForm(request.POST)
                    
                    if form.is_valid():
                        orden.valoracion_Cliente = valoracion
                        orden.resegna_Cliente = resegna
                        orden.save()
                        actualizarValoracionProfesional(profesional.id)
                    else:
                        data['error'] = form.errors
                    
            elif request.POST['action'] == 'EscribirResegna':
                usuario = User.objects.get(pk=request.user.id)
                
                form = ValorarEmpresaForm(request.POST)
                
                if form.is_valid():
                        resegna = ResegnaEmpresa(mensaje=request.POST['mensaje'],valoracion =request.POST['valoracion'],usuario_id =request.user.id)   
                        resegna.save()
                else:
                    data['error'] = form.errors
                

                       
  
            else:
                data['error'] = "No has seleccionado ninguna accion"

        except Exception as e:
            data ={"error":str(e)}
    
      
        return JsonResponse(data,safe=False)

class EditarClienteView(LoginRequiredMixin,FormView):
    template_name= "OficinaCliente/editarCliente.html"
    success_url = reverse_lazy("OficinaCliente:perfil")
    form_class=EditarClienteForm

    
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

        
    def get_form(self,form_class=None):
        
        user = User.objects.get(pk=self.request.user.id)
        resegna = None
        valoracion = 0
        if ResegnaEmpresa.objects.filter(usuario_id=self.request.user.id).exists():
            data = ResegnaEmpresa.objects.get(usuario_id=self.request.user.id)
            resegna = data.mensaje
            valoracion = data.valoracion
            


        form = EditarClienteForm(initial={
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'callePrincipal':user.callePrincipal,
            'entreCalle1':user.entreCalle1,
            'entreCalle2':user.entreCalle2,
            'numeroDeLaCasa':user.numeroDeLaCasa,
            'first_name':user.first_name,
            'provincia':user.provincia,
            'municipio':user.municipio,

            'resegna':resegna,
            'valoracion':valoracion,
            })
        return form

    def post(self,request,*args,**kwargs):

        data={}
        
        form = EditarClienteForm(data=request.POST)
        try:

            usuario = User.objects.get(pk=self.request.user.id)

            if request.POST['action']== 'editar':
                
                if form.is_valid():
                    
                    nombreUsuario= form.cleaned_data['username']
                    email= form.cleaned_data['email']
                    nombre = form.cleaned_data['first_name']
                    apellido = form.cleaned_data['last_name']
                    calleP = form.cleaned_data['callePrincipal']
                    entreC1 = form.cleaned_data['entreCalle1']
                    entreC2 = form.cleaned_data['entreCalle2']
                    numero = form.cleaned_data['numeroDeLaCasa']
                    provincia = form.cleaned_data['provincia']
                    municipio = form.cleaned_data['municipio']
                    mensajeResegna = form.cleaned_data['resegna']
                    valoracion = form.cleaned_data['valoracion']
                    direccion= "{0},{1}, Calle {2} / Calle {3} y Calle {4} No {5}".format(provincia,municipio,calleP,entreC1,entreC2,numero)

              
                    if(mensajeResegna):
                        resegna = ResegnaEmpresa.objects.get(usuario_id=self.request.user.id)
                        resegna.mensaje= mensajeResegna
                        resegna.valoracion=valoracion
                        resegna.save()
                    

                    usuario.username = nombreUsuario
                    usuario.email = email
                    usuario.first_name = nombre
                    usuario.last_name = apellido
                    usuario.callePrincipal = calleP
                    usuario.entreCalle1 = entreC1
                    usuario.entreCalle2 = entreC2
                    usuario.numeroDeLaCasa = numero
                    usuario.direccion = direccion
                    usuario.provincia=provincia
                    usuario.municipio=municipio
                    #usuario.resegna=resegna
                    usuario.save()
                   
                    
                else:
                    data['error']=form.errors
                
            elif request.POST['action']== 'autocomplete':
                data=[]
                
                
                for i in Municipio.objects.filter(nombre__icontains = request.POST['term'],provincia_id=request.POST['id']).values():
                    i['text']=i['nombre']
                    
                    data.append(i)


            else:
                data['error']='No ha seleccionado ninguna accion' 


        except Exception as e:
            data['error']=str(e)

         

        return JsonResponse(data,safe=False)
    
    def get_context_data(self,*args,**kwargs):
        Valoracion = 0
        Mensaje = None
        if ResegnaEmpresa.objects.filter(usuario_id=self.request.user.id).exists():
            data =ResegnaEmpresa.objects.get(usuario_id=self.request.user.id)
            Mensaje = data.mensaje
            Valoracion = data.valoracion


        context=super().get_context_data(*args,**kwargs)
        context['url_reverse'] =reverse_lazy("OficinaCliente:perfil")
        context['url_ok'] = self.success_url
        context['Valoracion'] = str(Valoracion)
        context['Mensaje'] = Mensaje
      
        return context

class CrearOrdenView(LoginRequiredMixin,CreateView):
    model = Orden
    form_class = OrdenForm
    template_name= "OficinaCliente/crearOrden.html"
    success_url = reverse_lazy("OficinaCliente:perfil")

    def get(self, request,id_servicio ,*args, **kwargs):

      servicio = Servicio.objects.get(id = id_servicio)
      usuario = self.request.user
      url_reverse =reverse_lazy("OficinaCliente:servicios")
      url_ok = self.success_url
      form = self.form_class(initial={'cliente': usuario.id, 'tipoDeServicio':id_servicio,'estado':'Pendiente'})

      return render(request, self.template_name, {'form': form , 'url_ok': url_ok, 'url_reverse': url_reverse,'servicio':servicio})
    
    def post(self,request,*args,**kwargs):
        data={}

        try:
            form = self.get_form()

            if form.is_valid():
                form.save()
                               
            else:
                data['error']=form.errors
                
        
        
        except Exception as e:
            data['error']=str(e)

         

        return JsonResponse(data)

class CambiarPassView(LoginRequiredMixin,PasswordChangeView):
    template_name= "OficinaCliente/cambiarPass.html"
    success_url = reverse_lazy("OficinaCliente:perfil")
    form_class=CambiarPassForm

    def post(self,request,*args,**kwargs):

        data={}

        try:
            form = self.get_form()

            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                               
            else:
                data['error']=form.errors
                
        
        
        except Exception as e:
            data['error']=str(e)

         

        return JsonResponse(data)
    
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['url_reverse'] =reverse_lazy("OficinaCliente:perfil")
        context['url_ok'] = self.success_url
      
        return context



class BuzonView(LoginRequiredMixin,TemplateView):
    template_name = 'OficinaCliente/buzon.html'


    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        data={}
       
      
        try:


            if request.POST['action'] == 'listar':
                data=[]
                
                ListadoNotificaciones = Notificacion.objects.filter(usuario_id = self.request.user.id).values()

                for i in ListadoNotificaciones:
                    data.append(i)
            else:
                data['error'] = "No has seleccionado ninguna accion"

        except Exception as e:
            data ={"error":str(e)}
    
      
        return JsonResponse(data,safe=False)
    
    
    def get_context_data(self,*args,**kwargs):
        context= super().get_context_data(*args,**kwargs)
        context['breadcrumbs']='Buzon de Notificaciones'
        return context

class LeerNotificacionView(LoginRequiredMixin,DetailView):
    template_name = 'OficinaCliente/leer_notificacion.html'
    model = Notificacion

    
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)
  


    def post(self,request,*args,**kwargs):
        data={}
       
      
        try:

            if request.POST['action'] == 'CargarDatos':
                objeto = self.get_object()
                
                data={'titulo':objeto.titulo,'mensaje':objeto.mensaje,'categoria':objeto.categoria,'fecha':objeto.fecha}
                
                if(objeto.leido == False):
                    objeto.leido = True
                    objeto.save(update_fields=['leido'])

               
            else:
                data['error'] = "No has seleccionado ninguna accion"

        except Exception as e:
            data ={"error":str(e)}
    
      
        return JsonResponse(data)


    def get_context_data(self,*args,**kwargs):
        objeto = self.get_object()
        context= super().get_context_data(*args,**kwargs)
        return context