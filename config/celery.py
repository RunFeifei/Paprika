from datetime import timedelta

from celery import Celery

from config.common import app

app.config['BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
app.config['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']
app.config['REDIS_URL'] = 'redis://localhost:6379'
app.config['JSON_AS_ASCII'] = False
celery = Celery(app.name)

celery.conf.update(app.config)
celery.conf.CELERYBEAT_SCHEDULE = {
    "test": {
        "task": "get_cron",
        "schedule": timedelta(seconds=10)
    }
}
from config.socket import socketio


@celery.task(name="get_cron")
def get_cron():
    get_sendback.delay()


@celery.task()
def get_sendback():
    socketio.emit('sendback', 'message', broadcast=True)


def config_app_celery():
    return celery
