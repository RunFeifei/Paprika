# Paprika
基于Flask-RESTful、Flask-JWT-Extended、Flask-SQLAlchemy在Flask框架下实现的微API服务  
#### 接入socketIO中
A.启动celery:  
celery -A config.celery.celery worker -l info -P eventlet  
B.启动socket:  
python3 app.py  
C.执行定时任务:  
celery -A manage.celery beat --loglevel=debug