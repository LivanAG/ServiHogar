
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import * 
from django.contrib.auth import views as auth_views
app_name = "OficinaCliente"

urlpatterns = [
    path('Home/',HomeView.as_view(), name="home"),
    path('Servicios/',ServiciosView.as_view(), name="servicios"),
    path('ProfesionalInfo/',ProfesionalInfoView.as_view(),name='prof_info'),
    path('Perfil/',PerfilView.as_view(), name="perfil"),
    path('CrearOrden/<int:id_servicio>',CrearOrdenView.as_view(), name="crear_orden"),
    path('CambiarPass/',CambiarPassView.as_view(),name='pass'),
    path('EditarCliente/',EditarClienteView.as_view(),name='editarCliente'),
    path('Buzon/',BuzonView.as_view(),name='buzon'),
    path('LeerNotificacion/<pk>',LeerNotificacionView.as_view(),name='leer'),
]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
