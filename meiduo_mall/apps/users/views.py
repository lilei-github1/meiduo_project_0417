from django.shortcuts import render
from django.views import View
from apps.users.models import User
from django import http
import logging,json,re
from django.contrib.auth import login
#日志输出器
logger = logging.getLogger('django')
# Create your views here.

class RegisterView(View):
    """用户注册"""
    """实现注册逻辑"""
    #接收参数：请求体中的JSON数据
    def post(self,request):
        #用户注册
        #POST http://www.meiduo.site:8000/register/
        json_byts = request.body
        json_str = json_byts.decode()
        #讲JSON字符串，转成python的标准字典
        json_dict = json.loads(json_str)
        #提取参数
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        allow = json_dict.get('allow')
        #校验参数
        if not all([username,password,password2,mobile,allow]):#只要列表中有一个元素为空，那么就返回false,都不为空，返回true
            return http.JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        #判断用户名是否满足项目的格式要求
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            #如果用户名不满足格式要求，返回错误信息，立马终止逻辑
            return http.JsonResponse({'code':400,'errmsg':'参数username有误'})
        # 判断密码是否满足项目的格式要求
        if not re.match(r'^[a-zA-Z0-9_-]{8,20}$',password):
            # 如果密码不满足格式要求，返回错误信息，立马终止逻辑
            return http.JsonResponse({'code': 400, 'errmsg': '参数password有误'})
        #判断密码password与password2是否相等
        if password != password2:
            return http.JsonResponse({'code': 400,
                                      'errmsg': '两次输入不对'})
        # 判断手机号是否满足项目的格式要求
        if not re.match(r'^1[3-9]\d{9}$', mobile):
                # 如果密码不满足格式要求，返回错误信息，立马终止逻辑
            return http.JsonResponse({'code': 400, 'errmsg': '参数mobile有误'})
        #判断是否勾选协议
        if allow != True:
                # 如果未勾选协议，返回错误信息，立马终止逻辑
            return http.JsonResponse({'code': 400, 'errmsg': 'allow格式有误'})


#实现核心逻辑：保存注册数据到用户数据表
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':400,'errormsg':'注册失败'})

        #用于实现登录，注册保持状态
        login(request,user)

#实现状态保持：因为美多商城的需求是注册成功即登录
#响应结果
        return http.JsonResponse({'code':0,'error':'注册成功'})



class UsernameCountView(View):
    def get(self,request,username):
        try:
            user = count = User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': '400', 'errmsg': '数据错误',})
        return http.JsonResponse({'code':'0','errmsg':'OK','count':count})


