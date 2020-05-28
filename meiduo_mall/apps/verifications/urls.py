from django.urls import path
from . import views


urlpatterns = [
# """图形验证码
#     GET http://www.meiduo.site:8000/image_codes/-e29b-41d4-a716-446655440000/"""
    path('image_codes/<uuid:uuid>/',views.ImageCodeView.as_view),

    path('sms_codes/<mobile:mobile>/',views.SMSCodeView.as_view()),
]