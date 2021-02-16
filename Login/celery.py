from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ServiHogar2.settings')


app = Celery('celery')

app.config_from_object('Login.celery_config')



