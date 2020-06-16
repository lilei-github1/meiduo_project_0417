# #celery入口文件
# # 从你刚刚下载的包中导入 Celery 类
# from celery import Celery
#
# #创建实例
# # 利用导入的 Celery 创建对象，
# #meiduo为别名
# celery_app = Celery('meiduo')
# #加载配置
# celery_app.config_from_object('celery_tasks.config')
#
#
#
# # 让 celery_app 自动捕获目标地址下的任务:
# # 就是自动捕获 tasks
# #注册异步任务
# celery_app.autodiscover_tasks(['celery_tasks.sms','celery_app.email'])


# Celery的入口文件
from celery import Celery


# 在创建celery实例之前，把Django的配置模块加载到运行环境中
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'


# 创建Celery实例
# Celery('别名')
celery_app = Celery('meiduo')

# 加载配置
# celery_app.config_from_object('配置文件')
celery_app.config_from_object('celery_tasks.config')

# 注册异步任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email'])