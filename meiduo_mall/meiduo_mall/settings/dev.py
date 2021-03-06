#开发环境
"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
#查看美多商城的导包路径
import sys
#查看美多商城的导包路径
# print(sys.path)
"""
['/home/ubuntu/Desktop/meiduo_project_0417/meiduo_mall',
 '/home/ubuntu/software/pycharm-2019.1.3/helpers/pydev', 
 '/home/ubuntu/Desktop/meiduo_project_0417', 
 '/home/ubuntu/software/pycharm-2019.1.3/helpers/pycharm_display', 
 /home/ubuntu/software/pycharm-2019.1.3/helpers/third_party/thriftpy', 
 '/home/ubuntu/software/pycharm-2019.1.3/helpers/pydev', 
 '/home/ubuntu/.PyCharm2019.1/system/cythonExtensions',
  '/home/ubuntu/Desktop/meiduo_project_0417/meiduo_mall', 
  '/home/ubuntu/.virtualenvs/py_django/lib/python36.zip',
   '/home/ubuntu/.virtualenvs/py_django/lib/python3.6', 
   '/home/ubuntu/.virtualenvs/py_django/lib/python3.6/lib-dynload', 
   '/usr/lib/python3.6', 
   '/home/ubuntu/.virtualenvs/py_django/lib/python3.6/site-packages',
    '/home/ubuntu/software/pycharm-2019.1.3/helpers/pycharm_matplotlib_backend']
/home/ubuntu/Desktop/meiduo_project_0417/meiduo_mall/meiduo_mall
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j+@i4lrx47j5$i^lc9#qbq%u!-907nawsl7nsp(6h%0ccu_k01'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',#用户模块
    'corsheaders',#解决跨域的,注册跨域的子应用
    'apps.verifications',#验证模块
    'apps.oauth',#第三方登录
    'apps.areas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',注释掉，保证非GET请求可以正常发送
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',#添加中间件


]
#添加跨域的白名单
CORS_ORIGIN_WHITELIST  = [
     "http://www.meiduo.site:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8080"
]
#允许跨域时携带cookie
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # 数据库引擎
        'HOST': '127.0.0.1', # 数据库主机
        'PORT': 3306, # 数据库端口
        'USER': 'itcast_0417', # 数据库用户名
        'PASSWORD': '123456', # 数据库用户密码
        'NAME': 'meiduo_0417' # 数据库名字
    }
}
#配置redis后端
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
        # 我的需求是希望将session存储在redis的1号库
        "session": {  # session后端
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        "verify_code": {  # 验证码
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # 将来还会继续在这里追加配置:用户浏览记录，购物车
}

#配置sesson后端
SESSION_ENGINE = "django.contrib.sessions.backends.cache"#修改redis存储为
SESSION_CACHE_ALIAS = "session"#存储session数据是使用的配置别名

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

#配置日志
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

#指定django默认扥用户模型为自定义的用户模型类
AUTH_USER_MODEL = "users.User"


# QQ登录参数
QQ_CLIENT_ID = '101474184' # 我们申请的 客户端id
QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c' # 我们申请的 客户端秘钥
QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html' # 登录成功后回调的路径

# 配置邮件服务器：send_mail()方法会去使用这些配置参数，连接到SMTP服务器上
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 指定邮件后端
EMAIL_HOST = 'smtp.163.com' # 发邮件主机
EMAIL_PORT = 25 # 发邮件端口
EMAIL_HOST_USER = 'hmmeiduo@163.com' # 授权的邮箱
EMAIL_HOST_PASSWORD = 'hmmeiduo123' # 邮箱授权时获得的密码，非注册登录密码
EMAIL_FROM = '美多商城<hmmeiduo@163.com>' # 发件人抬头


# 邮箱激活链接
EMAIL_VERIFY_URL = 'http://www.meiduo.site:8080/success_verify_email.html?token='
