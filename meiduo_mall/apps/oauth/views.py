from django.shortcuts import render
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from django.conf import settings
from django import http
from django.contrib.auth import login
from apps.oauth.models import OAuthQQUser
# Create your views here.
class QQUserView(View):
    """
    处理授权后的回调逻辑
    GET:/oauth_callback/
    """

    def get(self,request):
        # 获取code
        code = request.GET.get('code')
        if not code:
            return http.JsonResponse({'code':400,'errmsg':'缺少code'})

        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 携带 code 向 QQ服务器 请求 access_token
            access_token = oauth.get_access_token(code)

            # 携带 access_token 向 QQ服务器 请求 openid
            openid = oauth.get_open_id(access_token)

        except Exception as e:
            # 如果上面获取 openid 出错, 则验证失败
            # logger.error(e)
            # 返回结果
            return http.JsonResponse({'code': 400,'errmsg': 'oauth2.0认证失败, 即获取qq信息失败'})
#         使用openid去判断当前的QQ用户是否已经绑定过美多商城的用户
        try:

            oauth_model = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNoteExist:
            pass
        else:
            # openid已绑定美多商城的用户：直接实现状态保持即可
            # 提示：在实现QQ登录时，真正登录到美多商城的不是QQ用户，而是QQ用户绑定的美多商城用户
            # login(request=request, user='跟openid绑定的美多商城的用户对象')
            login(request = request,user=oauth_model.user)
            response = http.JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username',oauth_model.user.username,max_age=3600*24*14)
            return response
        pass
class QQURLView(View):
    """提供QQ登录页面网址"""
    # GET:/qq/authorization/

    def get(self, request):
        # next 表示从哪个页面进入到的登录页面
        # 将来登录成功后，就自动回到那个页面
        # 接收next参数
        next = request.GET.get('next','/')

        # 获取 QQ 登录页面网址
        # 创建 OAuthQQ 类的对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=next)
  # 调用对象的获取 qq 地址方法
        login_url = oauth.get_qq_url()

        # 返回登录地址
        return http.JsonResponse({'code': 0,
                                  'errmsg': 'OK',
                                  'login_url':login_url})