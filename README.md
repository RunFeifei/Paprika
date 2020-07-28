# Paprika
基于Flask-RESTful、Flask-JWT-Extended、Flask-SQLAlchemy在Flask框架下实现的微API服务  
#### 接入socketIO中
启动celery:  
celery -A config.celery.celery worker -l info -P eventlet