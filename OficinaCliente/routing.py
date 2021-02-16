from django.urls import re_path

from .consumers import *

web_sockets_urlpatterns =[ 

    re_path('ws/revision/', RevisionConsumer.as_asgi()),

]