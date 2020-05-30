#celery配置文件

#指定消息队列：使用redis数据库
# 如果使用 redis 作为中间人
# 需要这样配置:
broker_url='redis://127.0.0.1:6379/3'