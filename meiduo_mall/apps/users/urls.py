from django.urls import path

from . import views


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
]