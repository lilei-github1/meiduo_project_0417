from django.urls import path
from . import views


urlpatterns = [

    #判断用户名是否重复注册：GET /usernames/itcast/count/
    path('usernames/<username：username>/count/',views.UsernameCountView.as_view()),
    #用户注册：POST http：//www.meiduo.site:8000/register
    path('register/',views.RegisterView.as_view()),
]