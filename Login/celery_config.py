


broker_url = 'redis://localhost:6379/0'

imports = ['Login.tareas']
#include = ['Login.tareas']

result_backend = 'redis://localhost'

timezone = 'UTC'

result_serializer = 'json'

beat_schedule = {

    'revision-every-30-seconds': {
        'task': 'Login.tareas.revision',
        'schedule': 5.0,
    },
}