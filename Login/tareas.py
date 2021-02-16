from .celery import app
from datetime import datetime


def avisar_al_websocket():
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("hola",{"type": "ActualizarDinamico",})

def Notificar_Eliminacion_de_Orden(instancia):
    from .models import Notificacion,User
    user = User.objects.get(pk=instancia.cliente_id)
    Notificacion.objects.create(
    usuario=user,
    categoria='Alerta',
    titulo="Orden Eliminada",
    mensaje='Hola '+user.first_name+'<br><br>Lamentamos informarle que su orden ha sido eliminada, ya que ningun profesional la ha tomado por falta de disponibilidad.<br>Disculpe las molestias ocasionadas, por favor intente de nuevo'
    )
    avisar_al_websocket()
    


@app.task
def revision():
    from .models import Notificacion,User
    from OficinaCliente.models import Orden
    hoy = datetime.now()
    
    for i in Orden.objects.filter(estado='Pendiente'):
        if i.FechaLimite<hoy:
            Notificar_Eliminacion_de_Orden(i)
            i.delete()

    return "Todo Bien"



