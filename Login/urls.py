
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import * 

app_name = "Login"

urlpatterns = [
    path('Index/',IndexView.as_view(), name="index"),
    path('Login/',IniciarSesionView.as_view(), name="login"),
   
    path('Registrar/',RegisterView.as_view(), name="registrar"),
    
    path('CerrarSesion/',LogoutView.as_view(), name="logout"),
    
    path('Resetear/Contraseña/',ResetPassView1.as_view(), name="reset1"),
    path('Cambiar/Contraseña/<str:token>',ResetPassView2.as_view(), name="reset2"),
    path('Prueba/',PruebaView.as_view(), name="prueba"),

   
]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
