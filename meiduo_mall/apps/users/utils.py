from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings

def generate_email_verify_url(user):
    s = Serializer(settings.SECRET_KEY,3600*24)
    data = {'user_id':user.id,'email':user.email}
    token = s.dumps(data).decode()
    # 返回邮箱激活链接
    # verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
    verify_url = settings.EMAIL_VERIFY_URL + token
    return verify_url