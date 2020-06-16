from django.shortcuts import render
from django.views import View
from django import http
import logging, json, re
from django.contrib.auth import login,authenticate,logout
from django_redis import get_redis_connection
from apps.users.models import User
from meiduo_mall.utils.views import LoginRequiredJSONMixin
from celery_tasks.email.tasks import send_email_verify_url

# Create your views here.


# 日志输出器
logger = logging.getLogger('django')


class EmailView(LoginRequiredJSONMixin,View):
    '''添加邮箱'''
    def put(self,request):
        '''实现添加邮箱的逻辑'''
        #接收参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')
        # 校验参数
        if not email:
            return http.JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return http.JsonResponse({'code':400,'errmsg':'参数email格式错误'})

        # 实现核心逻辑
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code':400,'errmsg':'添加邮箱失败'})
        verify_url = '测试链接'
        send_email_verify_url.delay(email,verify_url)
        return http.JsonResponse({'code':0,'errmsg':'OK'})

class UserInfoView(LoginRequiredJSONMixin,View):
    """用户中心
    GET /info/
    """

    def get(self, request):
        """实现用户中心数据展示"""
        data_dict = {
            'code': 0,
            'errmsg': 'OK',
            'info_data': {
                'username': request.user.username,
                'mobile': request.user.mobile,
                'email': request.user.email,
                'email_active': request.user.email_active
            }
        }
        return http.JsonResponse(data_dict)
class LogoutView(View):
    """退出登录
    DELETE /logout/
    """

    def delete(self, request):
        """实现退出登录的逻辑
        提示:
            退出登录的逻辑正好跟登录相反的
            如果登录成功后，记住登录状态，那么退出登录就是清理登录状态
            如果登录成功后，将用户名写入到cookie，那么退出登录就需要清理用户名cookie
        """
        # 清理登录状态
        logout(request)

        # 清理用户名cookie
        response = http.JsonResponse({'code': 0, 'errmsg': '退出登录成功'})
        response.delete_cookie('username')

        return response


# 用户登录 GET:http://www.meiduo.site:8000/login/
class LoginView(View):
    def post(self,request):
        """实现用户登录逻辑"""
        #接收参数
        json_dict = json.loads(request.body.decode())

        account= json_dict.get('username')
        password = json_dict.get('password')
        remembered= json_dict.get('remembered')
        # 校验参数
        if not all([password,account]):
            return http.JsonResponse({'code':400,'errmsg':'缺少必传参数'})
        # if not re.match(r'^[a-zA-Z0-9_-]{8,20}$',account):
        #     return http.JsonResponse({'code':400,'errmsg':'参数username格式错误'})
        if not re.match(r'^[a-zA-Z0-9]{5,20}$', password):
            return http.JsonResponse({'code': 400, 'errmsg': '参数password格式错误'})



        #实现核心逻辑
        # 实现多账号登录
        if re.match(r'^1[3-9]\d{9}', account):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'
        # 认证登录用户核心思想：先使用用户名作为条件去用户表查询该记录是否存在，如果该用户名对应的记录存在，再去校验密码是否正确
        # 认证登录用户：Django的用户认证系统默认已经封装好了这个逻辑
        # 认证登录用户：仅仅是为了证明当前的用户是美多商城之前的注册用户，而且密码没错

        user = authenticate(request =request,username =account,password =password)

        if not user:
            return http.JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})

        #实现状态保持
        login(request,user)
        #还需要根据remembered参数去设置状态保持的周期
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)

        # 在登录成功后，将用户名写入到cookie，将来会在页面右上角展示
        response = http.JsonResponse({'code': 0, 'errmsg': '登录成功'})
        response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        #响应结束
        return response


class RegisterView(View):
    """用户注册
    POST http://www.meiduo.site:8000/register/
    """

    def post(self, request):
        """实现注册逻辑"""
        # 接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode() # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str) # 将JSON字符串，转成python的标准字典
        # json_dict = json.loads(request.body.decode())

        # 提取参数
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        # 提取短信验证码
        sms_code_client = json_dict.get('sms_code')
        allow = json_dict.get('allow')

        # 校验参数
        # 判断是否缺少必传参数
        # all([]): 判断某些数据中是否有为空的数据
        # 只要列表中元素有任意一个为空，那么就返回False，只有所有的元素不为空，才返回True
        # all([username, password, password2, mobile, allow])
        if not all([username, password, password2, mobile, allow]):
            # 如果缺少了必传参数，就返回400的状态码和错误信息，立马终止逻辑
            return http.JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        # 判断用户名是否满足项目的格式要求
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            # 如果用户名不满足格式要求，返回错误信息，立马终止逻辑
            return http.JsonResponse({'code': 400, 'errmsg': '参数username有误'})
        # 判断密码是否满足项目的格式要求
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            # 如果密码不满足格式要求，返回错误信息，立马终止逻辑
            return http.JsonResponse({'code': 400, 'errmsg': '参数password有误'})
        # 判断用户两次输入的密码是否一致
        if password != password2:
            return http.JsonResponse({'code': 400, 'errmsg': '两次输入不对'})
        # 判断手机号是否满足项目的格式要求
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'code': 400, 'errmsg': '参数mobile有误'})
        #实现多账号登录
        if not re.match(r'^1[3-9]\d{9}',username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 判断短信验证码是否正确：跟图形验证码的验证一样的逻辑
        # 提取服务端存储的短信验证码：以前怎么存储，现在就怎么提取
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_%s' % mobile) # sms_code_server是bytes
        # 判断短信验证码是否过期
        if not sms_code_server:
            return http.JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        # 对比用户输入的和服务端存储的短信验证码是否一致
        if sms_code_client != sms_code_server.decode():
            return http.JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})

        # 判断是否勾选协议
        if allow != True:
            return http.JsonResponse({'code': 400, 'errmsg': '参数allow有误'})

            # 实现核心逻辑：保存注册数据到用户数据表
            # 由于美多商城的用户模块完全依赖于Django自带的用户模型类
            # 所以用户相关的一切操作都需要调用Django自带的用户模型类提供的方法和属性
            # 其中就包括了保存用户的注册数据，Django自带的用户模型类提行了create_user()专门保存用户的注册数据
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': 400, 'errmsg': '注册失败'})
        # 实现状态保持：因为美多商城的需求是注册成功即登录成功
        # 我们记住当前的用户登录过的，cookie机制(不选的)，session机制（OK）
        # 如何证明当前的用户登录过，选择session机制，包含了记住登录状态和校验登录的状态
        # login()方法是Django提供的用于实现登录、注册状态保持
        # login('请求对象', '注册后或者登录认证后的用户')
        login(request, user)
        # 在注册成功后，将用户名写入到cookie，将来会在页面右上角展示
        response = http.JsonResponse({'code': 0, 'errmsg': '注册成功'})
        response.set_cookie('username',user.username,max_age=14*24*3600)

        # 响应结果：如果注册成功，前端会把用户引导到首页
        return response


class MobileCountView(View):
    """判断手机号是否重复注册
    GET http://www.meiduo.site:8000/mobiles/18500001111/count/
    """

    def get(self, request, mobile):
        """
        查询手机号对应的记录的个数
        :param mobile: 用户名
        :return: JSON
        """
        try:
            count= User.objects.filter(mobile=mobile).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': '400', 'errmsg': '数据错误'})

        return http.JsonResponse({'code': '0', 'errmsg': 'OK', 'count': count})


class UsernameCountView(View):
    """判断用户名是否重复注册
    GET http://www.meiduo.site:8000/usernames/itcast/count/
    """

    def get(self, request, username):
        """
        查询用户名对应的记录的个数
        :param username: 用户名
        :return: JSON
        """
        try:
            count= User.objects.filter(username=username).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': '400', 'errmsg': '数据错误'})

        return http.JsonResponse({'code': '0', 'errmsg': 'OK', 'count': count})
