
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import * 

app_name = "Profesional"

urlpatterns = [
 
    path('LoginProfesional/',LoginProfesionalView.as_view(), name="login_profesional"),
    path('OficinaProfesional/',OficinaProfesionalView.as_view(), name="oficina_profesional"),
    path('PerfilProfesional/',PerfilProfesionalView.as_view(), name="perfil_profesional"),

]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
