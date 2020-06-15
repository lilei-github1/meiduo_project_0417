from django.urls import path

from . import views
#


urlpatterns = [
    # 判断用户名是否重复注册:GET /usernames/itcast/count/
    # path('usernames/itcast/count/', views.UsernameCountView.as_view()),
    # path('usernames/<'匹配用户名的路由转换器:变量'>/count/', views.UsernameCountView.as_view()),
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),

    # 判断手机号是否重复注册:GET http://www.meiduo.site:8000/mobiles/18500001111/count/
    path('mobiles/<mobile:mobile>/count/', views.MobileCountView.as_view()),

    # 用户注册:POST http://www.meiduo.site:8000/register/
    path('register/', views.RegisterView.as_view()),
#用户登录 GET:http://www.meiduo.site:8000/login/
    path('login/',views.LoginView.as_view()),
# 退出登录：DELETE http://www.meiduo.site:8000/logout/
    path('logout/', views.LogoutView.as_view()),
# 用户中心：GET http://www.meiduo.site:8000/info/
    path('info/', views.UserInfoView.as_view()),
# 添加有相关：GET http://www.meiduo.site:8000/emails/
    path('emails/',views.EmailView.as_view()),

]