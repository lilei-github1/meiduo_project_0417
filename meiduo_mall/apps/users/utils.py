from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadData
from django.conf import settings
from apps.users.models import User

def generate_email_verify_url(user):
    s = Serializer(settings.SECRET_KEY,3600*24)
    data = {'user_id':user.id,'email':user.email}
    token = s.dumps(data).decode()
    # 返回邮箱激活链接
    # verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
    verify_url = settings.EMAIL_VERIFY_URL+token
    return verify_url
def check_email_verify_url(token):
    """
    反序列化用户信息密文
    :param token: 用户信息密文
    :return: 用户对象信息
    """
    # 创建序列化器对象
    s = Serializer(settings.SECRET_KEY, 3600*24)
    # 反序列化
    try:
        data = s.loads(token)
    except BadData:
        return None
    else:
        # 提取用户信息
        user_id = data.get('user_id')
        email = data.get('email')
        # 使用user_id和email查询对应的用户对象
        try:
            user = User.objects.get(id=user_id, email=email)
        except User.DoesNotExist:
            return None
        else:
            return user


