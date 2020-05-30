#celery入口文件
# 从你刚刚下载的包中导入 Celery 类
from celery import Celery

#创建实例
# 利用导入的 Celery 创建对象，
#meiduo为别名
celery_app = Celery('meiduo')
#加载配置
celery_app.config_from_object('celery_tasks.config')



# 让 celery_app 自动捕获目标地址下的任务:
# 就是自动捕获 tasks
#注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])