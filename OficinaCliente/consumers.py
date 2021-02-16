import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Login.models import *
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.core.signals import request_finished
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from OficinaCliente.models import *
 

@receiver(post_save,sender=Notificacion)
def Notificacion_leida(sender,update_fields,instance,**kwargs):
    if update_fields:
        for i in update_fields:
            if i == 'leido':
                print("aquiiiiiiii")



class RevisionConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.channel_layer.group_add('hola',self.channel_name)
        await self.accept()
        await self.actualizar()
        #await self.channel_layer.group_send("hola",{"type": "probar",})

        
    async def disconnect(self,close_code):
        print("Se desconecto el socket")
        await self.channel_layer.group_discard('hola',self.channel_name)

    async def receive(self,text_data):
        data = json.loads(text_data)       

        await self.send(text_data=json.dumps({'Mensaje': "dale que te vi"}))

    

    async def actualizar(self):
        #print("entrooooooooooooooo")
        await self.send(text_data=json.dumps({'Cantidad_de_Notificaciones': await self.actualizar_valor_cant_notificaciones()}))

    async def ActualizarDinamico(self,event):
        await self.actualizar()


  
    
    
    @database_sync_to_async    
    def actualizar_valor_cant_notificaciones(self):
        contador = Notificacion.objects.filter(leido=False,usuario_id=self.scope['user'].id).count()
        return contador


