from django.conf import settings
from django.shortcuts import render
from .models import *
from .forms import *
from .urls import *
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView,FormView
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf  import csrf_exempt
from django.http import JsonResponse
from django.urls  import reverse_lazy
from OficinaCliente.models import *
import smtplib
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from email.mime.multipart import MIMEMultipart
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid




class IndexView(TemplateView):
    template_name = "Login/index.html"
    
    def get_context_data(self,*args,**kwargs):
       
        lista_PorqueContratarNuestrosServicios ={
            "Conveniencia":"Es simple. Elegís fecha y horario, y recibís al profesional en tu domicilio",
            "Transparencia":"Evita sorpresas. Seleccioná el servicio que necesitas a un precio de mercado ya predefinido",
            "Calidad":"Calidad: Servicio garantizado. Todos los profesionales están verificados y son permanentemente evaluados",
            }
        
        parrafo_Acerca_de="RapiHogar es una red de profesionales dedicados a proveer servicios de reparación del hogar como cerrajería, electricidad, gas, plomería y albañilería, entre otros.Nos especializamos en la búsqueda de la opción más cercana y disponible para satisfacer tus necesidades mientras te proveemos seguridad a través de la verificación de la matrícula, experiencia y profesionalización de cada prestador." 
   
        lista_servicios = Servicio.objects.all()

        lista_FAQ = {
            "Puedo perder mi dinero sin que mi servicio sea completado?":"Feugiat pretium nibh ipsum consequat. Tempus iaculis urna id volutpat lacus laoreet non curabitur gravida. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non.",
            "Puedo pagar en efectivo, o solo puedo pagar por transferencia?":"Feugiat pretium nibh ipsum consequat. Tempus iaculis urna id volutpat lacus laoreet non curabitur gravida. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non.",
            "Es seguro pedir un servicio suyo, a traves de esta plataforma?":"Feugiat pretium nibh ipsum consequat. Tempus iaculis urna id volutpat lacus laoreet non curabitur gravida. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non.",
            "Que pasa si el profesional toma mi orden pero nunca aparece?":"Feugiat pretium nibh ipsum consequat. Tempus iaculis urna id volutpat lacus laoreet non curabitur gravida. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non.",
            "Que pasa si para el dia que encargo mi servicio no hay ningun profesional disponible? ":"Feugiat pretium nibh ipsum consequat. Tempus iaculis urna id volutpat lacus laoreet non curabitur gravida. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non.",
            "Como reaccionar en caso de no quedar satisfecha con el trabajo realizado por el profesional?":"Feugiat pretium nibh ipsum consequat. Tempus iaculis urna id volutpat lacus laoreet non curabitur gravida. Venenatis lectus magna fringilla urna porttitor rhoncus dolor purus non.",            
            }

        lista_trabajadores = Trabajador.objects.all()

        context=super().get_context_data(*args,**kwargs)
        context['lista_PorqueContratarNuestrosServicios']=lista_PorqueContratarNuestrosServicios
        context['parrafo_Acerca_de']=parrafo_Acerca_de
        context['lista_servicios']=lista_servicios
        context['lista_FAQ']=lista_FAQ
        context['lista_trabajadores']=lista_trabajadores
        return context


class RegisterView(FormView):
    template_name = "Login/register.html"
    form_class = FormRegistro
    success_url=reverse_lazy("Login:login")

    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        data={}

        
        try:
            form = FormRegistro(request.POST)
            
            if request.POST['action']== 'registrar':

                if form.is_valid():
                    form.save()
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
        context=super().get_context_data(*args,**kwargs)
        context['url_ok']=self.success_url
        return context


class IniciarSesionView(LoginView):
    template_name = "Login/login.html"
    form_class = LoginForm


class ResetPassView1(FormView):
    template_name = 'Login/reset_pass_1.html'
    form_class = PassReset1Form
    

    def enviar_mail(self,user):
        try:

            url = "" 
            
            """Comprobamos si el proyecto esta en fase de produccion, es decir el debug en true usamos 
               la direccion del HTTP_HOST de lo contrario buscamos la direccion puesta en nuestra variable domain en 
               settings
            """
            if settings.DEBUG == False:
                url= settings.DOMAIN
            else:
                url= self.request.META['HTTP_HOST']

      
            user.token = uuid.uuid4()
            user.save()

            # Establecemos conexion con el servidor smtp de gmail
            mailServer = smtplib.SMTP(settings.EMAIL_HOST,settings.EMAIL_PORT)
            print(mailServer.ehlo())# Comprueba si tenemos conexion y nos da la respuesta 
            mailServer.starttls() # Establece una conexion segura
            print(mailServer.ehlo())# Comprueba si tenemos conexion y nos da la respuesta 
            mailServer.login(settings.EMAIL_HOST_USER,settings.EMAIL_HOST_PASSWORD)

            email_to=user.email
            
            # Construimos el mensaje 
            mensaje = MIMEMultipart()
            mensaje['From']=settings.EMAIL_HOST_USER
            mensaje['To']=email_to
            mensaje['Subject']="Reseteo de Contrasena"
        
            content =  render_to_string('Login/plantilla_email.html',{
                "user":user,
                "link_resetpwd":'http://{}/Cambiar/Contraseña/{}'.format(url,str(user.token)),
                "link_home":'http://{}/Index/'.format(url),
            })

            mensaje.attach(MIMEText(content,'html')) #definimos el cuerpo del correo
            
            # Envio del mensaje
            mailServer.sendmail(settings.EMAIL_HOST_USER,"livanar00@gmail.com",mensaje.as_string())

        except Exception as e:
            print(e)

    def post(self, request,*args,**kwargs):
        data={}

        form = self.get_form()

        try:
            if form.is_valid():
                user = form.get_user()
               
                self.enviar_mail(user)
            else:
                data['error']=form.errors

        except Exception as e:
            data['error']=str(e)
        
        return JsonResponse(data)

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['url_ok'] =reverse_lazy("Login:login")
        context['url_reverse'] =reverse_lazy("Login:login")
        return context



class ResetPassView2(FormView):
    template_name= "Login/reset_pass_2.html"
    success_url = reverse_lazy("Login:login")
    form_class=PassReset2Form

    def dispatch(self,request,*args,**kwargs):
        if User.objects.filter(token=self.kwargs['token']).exists():
            return super().dispatch(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/Index/')
        

    def get_form(self,form_class=None):
        form = PassReset2Form(user=User.objects.get(token=self.kwargs['token']))
        return form

    def post(self,request,*args,**kwargs):

        data={}
        user=User.objects.get(token=self.kwargs['token'])

        try:
            
            form = PassReset2Form(user=user, data=request.POST)
            
            if form.is_valid():
                user.token = None
                user.save()
                form.save()
              
                               
            else:
                data['error']=form.errors
             
                    
        except Exception as e:
            data['error']=str(e)

         

        return JsonResponse(data)
    
    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['url_reverse'] =reverse_lazy("Login:index")
        context['url_ok'] = self.success_url
      
        return context




class PruebaView(TemplateView):
    template_name="Login/prueba.html"

    def get_context_data(self,*args,**kwargs):
        context=super().get_context_data(*args,**kwargs)
        context['form']=FormRegistro
        return context


