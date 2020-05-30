#celery入口文件
# 从你刚刚下载的包中导入 Celery 类
from celery import Celery

#创建实例
# 利用导入的 Celery 创建对象，
#meiduo为别名
celery_app = Celery('meiduo')
#加载配置
celery_app.config_from_object('celery_tasks.config')
