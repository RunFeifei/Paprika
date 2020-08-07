from datetime import timedelta

from celery import Celery

from config.common import app

app.config['BROKER_URL'] = 'redis://localhost:6379'  # 使用Broker作为消息代理
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'  # 把任务结果存在了Redis
app.config['CELERY_TASK_SERIALIZER'] = 'json'  # 任务序列化和反序列化使用json方案
app.config['CELERY_RESULT_SERIALIZER'] = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
app.config['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']  # 指定接受的内容类型
app.config['REDIS_URL'] = 'redis://localhost:6379'
app.config['JSON_AS_ASCII'] = False


def make_celery():
    celeryLocal = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['BROKER_URL']
    )
    celeryLocal.conf.update(app.config)

    celeryLocal.conf.CELERYBEAT_SCHEDULE = {
        'test': {
            'task': 'heart_beat',
            'schedule': timedelta(seconds=3)
        }
    }

    class ContextTask(celeryLocal.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celeryLocal.Task = ContextTask
    return celeryLocal


celery = make_celery()


def config_app_celery():
    return celery


######################CELERY#######################################


# callback=ack 不适用与celery?
# 拿到task id轮询状态如果失败就重试?
@celery.task(name='heart_beat')
def heart_beat():
    result = async_emit_msg.delay('heart_beat', 'beat', broadcast=True)
    print('heart_beat_result----{}----{}'.format(result.id, result.state))


# 怎么获取任务结果
# 怎么知道该任务是够已经完成
@celery.task()
def async_emit_msg(event, *args, **kwargs):
    from config.socket import socketio
    socketio.emit(event, *args, **kwargs)


"""
@socketio.on('testroom')
def test_room():
    app.logger.info('#########testroom#########')
    # 只有room0收到了
    emit('room', request.sid + ' has entered the room.', room='room0')
    # 只有room0收到了
    emit('room', 'emit to all rooms', )
    # 未加入room也收到了
    emit('room', 'broadcast to all rooms', broadcast=True)
"""
