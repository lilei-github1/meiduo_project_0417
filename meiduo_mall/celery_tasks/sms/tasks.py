#定义任务
#
from celery_tasks.sms.yuntongxun.ccp_sms import CCP
from celery_tasks.main import celery_app
#使用装饰器
@celery_app.task(name='ccp_send_sms_code')
def ccp_send_sms_code(mobile,sms_code):
    """发短信的异步任务"""
    ret = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    return ret
