"""
Django settings for Doraemon project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import pymysql

pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

VERSION = "0.1.0-dev"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-t2_02_pkgm=%9+k4ht8c*5m9)z@0qcsx38g&=s$#di)cbmys8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "xoo.site",
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "Doraemon",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件
    "Doraemon.middlewares.ClientInfoMiddleware",
]

ROOT_URLCONF = 'Doraemon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "template", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Doraemon.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    # 开发使用
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 生产使用
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'Doraemon',
    #     'USER': 'root',
    #     'PASSWORD': 'lujianxin.com',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    #     'CONN_MAX_AGE': 60 * 60 + 10
    # }
}

REDIS_AUTH = {
    "ip": "127.0.0.1",
    "password": "lujianxin.com",
    "port": 6379,
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'STATIC'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
GOTO_URL = "goto/"

# AUTH_USER_MODEL = 'Doraemon.Account'
AUTHENTICATION_BACKENDS = (
    'Doraemon.auth.EmailUsernameAuthBackend',  # 使用用户名或密码登录
    # 'Doraemon.auth.QQAuthBackend',  # QQ第三方登录
    # 'Doraemon.auth.GithubAuthBackend',  # github 第三方登录
    # 'Doraemon.auth.WechatAuthBackend',  # 微信第三方登录
)

# 消息提醒类型
TASKS = (
    ('GROUP_MORNING', "早九点值班提醒"),
    ('GROUP_NIGHT', "晚六点值班提醒"),
    ('PROBLEM_MORNING', "早九点接待提醒"),
    ('PROBLEM_NOON', "中午14点接待提醒"),
    ('PROBLEM_NIGHT', "晚六点接待提醒"),
    ("HOUR_MONITOR", "每小时存活提醒"),
)

# 初始化系统配置
KEYS = [
    {"key": "SHOW_DUTY_DAYS", "value": "7", "remark": "首页显示的值班天数"},
    {"key": "UPGRADING", "value": "0", "remark": "网站是否处于维护状态"},
    {
        "key": "DUTY_LOOP",
        "value": "['hailong.wang','xinyi.yang','tian.yuan','minghao.guan','futao.jiao','jeeyshe.lu','chenhui.shang','lei.xiao']",
        "remark": "轮班顺序"
    },
]

# ----------本站系统所用email配置----------
EMAIL_SUBJECT_PREFIX = "[Doraemon]"
SERVER_EMAIL = 'ido@xoo.site'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
EMAIL_USE_LOCALTIME = False

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = 'ido@xoo.site'
EMAIL_HOST_PASSWORD = 'xoo.site'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None

CACHES = {
    # 默认使用的库，session，csrf等存储
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_AUTH['ip']}:{REDIS_AUTH['port']}/9",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            "PASSWORD": REDIS_AUTH["password"],
        }
    },
}

SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# The path of the session cookie.
SESSION_COOKIE_PATH = '/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = not DEBUG

# 基于cache的缓存: redis
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
DJANGO_REDIS_IGNORE_EXCEPTIONS = True  # 忽略异常

LOGOUT_REDIRECT_URL = '/'
CSRF_USE_SESSIONS = True

# ------------simpleui配置

SIMPLEUI_HOME_TITLE = '哆啦A梦管理系统'
SIMPLEUI_LOGO = '/static/image/favicon.ico'
SIMPLEUI_HOME_INFO = True
SIMPLEUI_HOME_QUICK = True
SIMPLEUI_HOME_ACTION = True
SIMPLEUI_STATIC_OFFLINE = True
SIMPLEUI_LOGIN_PARTICLES = False  # 关闭登录页粒子动画
SIMPLEUI_ANALYSIS = False
SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menus': [
        {
            'name': '关于作者',
            'icon': 'fas fa-code',
            'url': 'https://me.lujianxin.com/'
        },
    ]
}

# ==========>logging<==========
LOGGING_PATH = BASE_DIR / 'logs'
if not Path(LOGGING_PATH).exists(): Path(LOGGING_PATH).mkdir()
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '[%(levelname)s][%(asctime)s] [%(filename)s] [%(module)s.%(funcName)s:%(lineno)d]-%(message)s'},
        # 简单格式
        'simple': {
            'format': '%(levelname)s %(funcName)s %(message)s'
        },
    },
    # 过滤
    'filters': {
        # 暂无过滤
    },
    # 定义具体处理日志的方式
    'handlers': {
        # 默认记录所有日志
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_PATH / 'Doraemon.log',
            'maxBytes': 1024 * 1024 * 10,  # 文件大小 10M
            'backupCount': 10,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_PATH / 'error.log',
            'maxBytes': 1024 * 1024 * 10,  # 文件大小
            'backupCount': 10,  # 备份数
            'formatter': 'standard',  # 输出格式
            'encoding': 'utf-8',  # 设置默认编码
        },
        # 控制台输出
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        # 输出info日志
        'info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_PATH / 'info.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'standard',
            'encoding': 'utf-8',  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    'loggers': {
        # 类型 为 django 处理所有类型的日志， 默认调用
        'django': {
            'handlers': ['default', 'console'],
            'level': 'INFO',
            'propagate': False,  # 是否轮转
        },
        # log 调用时需要当作参数传入
        'log': {
            'handlers': ['error', 'info', 'console', 'default'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
