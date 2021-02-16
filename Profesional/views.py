from django.shortcuts import render,redirect
from django.views.generic import TemplateView,FormView,ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from Login.forms import LoginForm
from django.contrib.auth import login,authenticate
from .models import *
from Login.models import *
from OficinaCliente.models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf  import csrf_protect,csrf_exempt
from django.http import JsonResponse
from datetime import datetime,timedelta,timezone
from django.contrib.auth.models import Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from email.mime.multipart import MIMEMultipart
from OficinaCliente.forms import ValorarForm


# Create your views here.

def actualizarValoracionProfesional(id):
    profesional = Profesional.objects.get(pk=id)
    lista = Orden.objects.filter(estado="Finalizado",profesional_id=id)
    total = 0
    contador = 0
    for i in lista:
        if i.valoracion_Cliente!=0:
            contador+=1
            total+=i.valoracion_Cliente
    

    profesional.valoracion = total/contador
    profesional.save()

    
def TituloService(i_d):
    serv = Servicio.objects.get(id=i_d)
    return serv.Titulo


class LoginProfesionalView(FormView):
    
    template_name = "Profesional/login_profesional.html"
    form_class = LoginForm

    def post(self,request,*args,**kwargs):
        
        form = self.get_form()

        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            id = User.objects.get(username=username).id
            
                

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)
            
            if user is not None:
                
                if Profesional.objects.all().filter(user_id=id).exists():

                    # Hacemos el login manualmente
                    login(request, user)
                    # Y le redireccionamos a la portada
                    return redirect('/OficinaProfesional/',args={'user':user})
                
                else:
                    msg = "Lo sentimos esta area es solo para profesionales!"
                    form.add_error('username', msg)
           
        return render(request, "Profesional/login_profesional.html", {'form': form})


class OficinaProfesionalView(LoginRequiredMixin,ListView):
    model = Orden
    template_name = "Profesional/oficinaProfesional.html"
    context_object_name="lista_ordenes"
    

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)


    
    def post(self,request,*args,**kwargs):
        data=[]
        pedro=[]
       
      
        try:
            if request.POST['action'] == 'listar':
                """
                Este metodo lista todas las ordenes pendientes actuales con las siguientes restricciones

                    1- Si un profesional pide un servicio relacionado con su categoria, logicamente a el no le va a aparecer como trabajo a escoger
                    2- Solo se listan las ordenes en dependencias a los permisos que tenga el profesional, es decir un porfesional con permiso de Jardineria solo le saldran ordenes de este tipo

                """
                # Capturando el profesional.
                profesional = Profesional.objects.get(user_id=self.request.user.id)
            
                # Identificando los permisos de trabajo del profesional.
                lista=[]
                lista_de_permisos = Permission.objects.filter(user=self.request.user)

                # Guardando en lista, los servicios que esta autorizado el profesional a impartir, segun los permisos que tiene
                for i in lista_de_permisos:
                    id =Servicio.objects.get(Titulo=i.name)
                    lista.append(id)

                # Capturando las ordenes que que sean Pendientes,que coincidan con los permisos del profesional, y que no tengan como cliente al profesional actual
                ListadoOrdenes = Orden.objects.filter(tipoDeServicio_id__in=lista,estado="Pendiente").values().exclude(cliente_id = self.request.user.id)
                
                # Creando la data para enviar por ajax a nuestro listar 
                for i in  ListadoOrdenes:
                    usuario = User.objects.get(id=i['cliente_id'])
                
                    id_orden = i['id']
                    tipoDeServicio = TituloService(i['tipoDeServicio_id'])
                    fecha = i['FechaLimite']
                    nombre = usuario.first_name
                    apellido = usuario.last_name
                    direccion = usuario.direccion
                    data.append({"id_orden":id_orden,"tipoDeServicio":tipoDeServicio,"fecha":fecha,"nombre":nombre,"apellido":apellido,"direccion":direccion})
                    

            elif request.POST['action'] == 'tomar':
              
                flag_Hay_Error = False
                profesional = Profesional.objects.get(user_id=self.request.user.id)
                
                
                #Capturando las ordenes que el profesional tiene en proceso
                ordenes_del_profesional_en_proceso= Orden.objects.filter(profesional_id=profesional.id)

                #Capturando la orden nueva a tomar
                orden=Orden.objects.get(id=request.POST['id'])

                #Tiempo que debe tener cada profesional entre trabajo y trabajo
                tiempo_minimo_de_diferencia_entre_trabajos = timedelta(hours=1)

                #Verificando si el profesional tiene alguna orden en proceso
                if ordenes_del_profesional_en_proceso:
                    for i in ordenes_del_profesional_en_proceso:
                        #Verificando si tiene alguna orden en proceso que sea en el mismo mes que la nueva
                        if i.FechaLimite.month == orden.FechaLimite.month:
                            
                            #Verificando si tiene alguna orden en proceso que sea en el mismo dia que la nueva
                            if i.FechaLimite.day == orden.FechaLimite.day:
                                
                                #Verificando la diferencia de hora entre una y otra
                                diferencia = abs(i.FechaLimite.hour - orden.FechaLimite.hour)
                                if diferencia<=2:
                                    flag_Hay_Error = True
                                    data = {'error': {'xx': ['No puedes tomar este trabajo.Ya tienes una orden en proceso este dia y a esta hora']}}
                                    
                if flag_Hay_Error == False:
                    orden.estado = 'En Proceso'
                    orden.profesional_id=profesional.id
                    orden.save()
                
                   

            else:
               data = {'error': {'xx': ['No has seleccionado ninguna accion']}}
            
		   
               

        except Exception as e:
            data ={"error":str(e)}
    

          
        return JsonResponse(data,safe=False)

    def get_context_data(self,*args,**kwargs):
        context= super().get_context_data(*args,**kwargs)
        context['breadcrumbs']='Trabajos'
        return context


class PerfilProfesionalView(LoginRequiredMixin,ListView):
    model = Orden
    template_name = "Profesional/perfilProfesional.html"
    context_object_name="lista_ordenes"
    

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self, request,*args, **kwargs):
        usuario = User.objects.get(pk=self.request.user.id)
        profesional = Profesional.objects.get(user_id=self.request.user.id)
        breadcrumbs ='Perfil'
        profesional.Trabajos_realizados = Orden.objects.filter(estado="Finalizado",profesional_id=profesional.id).count()
        profesional.save()
        return render(request, self.template_name, {'breadcrumbs': breadcrumbs, 'profesional': profesional, 'usuario': usuario,'form':ValorarForm})
    
    def post(self,request,*args,**kwargs):
        data={}
        pedro=[]
       
      
        try:
            if request.POST['action'] == 'listarEnProceso':
                data=[]

                profesional = Profesional.objects.get(user_id=self.request.user.id)
                
                for i in  Orden.objects.filter(estado="En Proceso",profesional_id=profesional.id).values():
                    usuario = User.objects.get(id=i['cliente_id'])
                            
                    id_orden = i['id']
                    tipoDeServicio = TituloService(i['tipoDeServicio_id'])
                    fecha = i['FechaLimite']
                    estado = i['estado']
                    nombre = usuario.first_name
                    apellido = usuario.last_name
                    direccion = usuario.direccion
                    profesional_TrabajoTerminado = i['profesional_TrabajoTerminado']
                    
                    data.append({"id_orden":id_orden,"tipoDeServicio":tipoDeServicio,"fecha":fecha,"nombre":nombre,"apellido":apellido,"direccion":direccion,"estado":estado,"profesional_TrabajoTerminado":profesional_TrabajoTerminado})
                    

            elif request.POST['action'] == 'listarFinalizados':
                data=[]

                profesional = Profesional.objects.get(user_id=self.request.user.id)
                #ListadoOrdenes = Orden.objects.filter(cliente_id=request.user.id,estado__in=['Pendiente','En Proceso']).values()
                
                for i in  Orden.objects.filter(estado="Finalizado",profesional_id=profesional.id).values():
                    usuario = User.objects.get(id=i['cliente_id'])
                
                    
                    id_orden = i['id']
                    tipoDeServicio = TituloService(i['tipoDeServicio_id'])
                    fecha = i['FechaLimite']
                    estado = i['estado']
                    nombre = usuario.first_name
                    apellido = usuario.last_name
                    direccion = usuario.direccion
                    profesional_TrabajoTerminado = i['profesional_TrabajoTerminado']
                    
                    data.append({"id_orden":id_orden,"tipoDeServicio":tipoDeServicio,"fecha":fecha,"nombre":nombre,"apellido":apellido,"direccion":direccion,"estado":estado,"profesional_TrabajoTerminado":profesional_TrabajoTerminado})
                    

            elif request.POST['action'] == 'CargarDatosPerfil':
                profesional = Profesional.objects.get(user_id=self.request.user.id)
                usuario = User.objects.get(pk=self.request.user.id)
                
                username = usuario.username
                nombre = usuario.first_name
                apellido = usuario.last_name
                email = usuario.email
                direccion = usuario.direccion
                valoracion = profesional.valoracion
                

                trabajosCompletados=Orden.objects.filter(estado="Finalizado",profesional_id=profesional.id).count()


                # Identificando los permisos de trabajo del profesional.
                lista=[]
                lista_de_permisos = Permission.objects.filter(user=self.request.user)

                # Guardando en lista, los servicios que esta autorizado el profesional a impartir, segun los permisos que tiene
                for i in lista_de_permisos:
                    lista.append(i.name)

                    
                data = {"username":username,"email":email,"trabajosCompletados":trabajosCompletados,"nombre":nombre,"apellido":apellido,"direccion":direccion,"permisos":lista,'valoracion':valoracion}
                 
            elif request.POST['action'] == 'completado':
                
                usuario = User.objects.get(pk=self.request.user.id)
               #Capturamos el profesional que ejecuto la llamada
                profesional = Profesional.objects.get(user_id=self.request.user.id)
                
                #Capturamos la orden que va a ser modificada
                orden = Orden.objects.get(id = request.POST['id'])
                

                if orden.profesional_TrabajoTerminado:
                    orden.profesional_TrabajoTerminado = False
                    orden.save()
                else:
                
                    if orden.cliente_TrabajoTerminado:
                        orden.profesional_TrabajoTerminado = True
                        orden.estado = "Finalizado"
                        orden.save()
                        profesional.Trabajos_realizados = Orden.objects.filter(estado="Finalizado",profesional_id=profesional.id).count()
                        profesional.save()
                        data={"contador":profesional.Trabajos_realizados}

                    
                    else:
                        orden.profesional_TrabajoTerminado = True
                        orden.save()
           
            elif request.POST['action'] == 'dejar':
            
               #Capturamos el profesional que ejecuto la llamada
                profesional = Profesional.objects.get(user_id=self.request.user.id)
                
                #Capturamos la orden que va a ser modificada
                orden = Orden.objects.get(id = request.POST['id'])
                

                orden.profesional=None
                orden.estado = 'Pendiente'  
                orden.save() 

            elif request.POST['action'] == 'valorarProfesional':
                from OficinaCliente.views import actualizarValoracionCliente
                orden = Orden.objects.get(pk=request.POST['id'])
                cliente = User.objects.get(pk = orden.cliente_id)

                if request.POST['action2'] == 'cargarModal':
                #Capturamos el profesional y la orden 
                    valoracionProfesional = orden.valoracion_Profesional
                    resegnaProfesional = orden.resegna_Profesional
                    data= {"valoracionProfesional":valoracionProfesional,"resegnaProfesional":resegnaProfesional,'id_orden':request.POST['id'],"nombre_cliente":cliente.first_name}
                elif request.POST['action2'] == 'salvarValoracion':
                    #Capturamos el profesional y la orden 
                    valoracion = request.POST['score']
                    resegna = request.POST['resegna']
                    form = ValorarForm(request.POST)
                    if form.is_valid():
                        orden.valoracion_Profesional = valoracion
                        orden.resegna_Profesional = resegna
                        orden.save()
                        actualizarValoracionCliente(cliente.id)
                    else:
                        data['error'] = form.errors
           
            else:
               data['error'] = 'No has seleccionado ninguna accion'
            
		   
               

        except Exception as e:
            data ={"error":str(e)}
    
        return JsonResponse(data,safe=False)




