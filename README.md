# Paprika
基于Flask-RESTful、Flask-JWT-Extended、Flask-SQLAlchemy在Flask框架下实现的微API服务  
#### 接入socketIO中
1 启动redis:  
redis-server  
2.启动celery:  
celery -A config.celery.celery worker -l info -P eventlet  
3.启动socket:  
python3 app.py  
4.执行定时任务:  
celery -A config.celery.celery beat --loglevel=debug  
#### 数据库
采用sqlite数据库,db文件在./config/sqlite.db  
#### Flower  
https://docs.celeryproject.org/en/stable/userguide/monitoring.html#flower-real-time-celery-web-monitor