# Paprika
基于Flask-RESTful、Flask-JWT-Extended、Flask-SQLAlchemy、SQLite、Flask-socketIO、Celery、Redis在Flask框架下实现的最小化API和IM的Server例子  
#### Android Client APP
[Android APP地址](https://github.com/RunFeifei/ASocketIOIM)  
#### 接入socketIO中
1 启动redis:  
redis-server  
2.启动celery:  
celery -A config.celery.celery worker -l info -P eventlet  
3.启动socket:  
python3 app.py  
4.执行定时任务:  
celery -A config.celery.celery beat --loglevel=debug  
5.启动Celery可视化工具Flower [配置](https://docs.celeryproject.org/en/stable/userguide/monitoring.html#flower-real-time-celery-web-monitor)  
celery -A config.celery.celery flower --broker=redis://localhost:6379  
#### 数据库
采用sqlite数据库,db文件在./config/sqlite.db  

