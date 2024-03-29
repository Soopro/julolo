# coding=utf-8
from __future__ import absolute_import

from datetime import timedelta
import os


class Config(object):

    # env
    DEBUG = True
    SECRET_KEY = 'gR9{(BA/xlS3+BMg3w73/B#vL3!wc('

    # path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DEPLOY_DIR = os.path.join(BASE_DIR, 'deployment_data')
    LOG_FOLDER = os.path.join(DEPLOY_DIR, 'log')
    TEMPORARY_FOLDER = os.path.join(DEPLOY_DIR, 'tmp')

    # url
    ALLOW_ORIGINS = ['*']
    ALLOW_CREDENTIALS = False
    DENIED_ORIGINS = []

    # analytics
    ONLINE_LAST_MINUTES = 30

    # content limit
    MAX_CONTENT_LENGTH = 64 * 1024 * 1024

    # file uploads
    ALLOWED_MEDIA_EXTS = ('jpg', 'jpeg', 'png')

    # JWT
    JWT_SECRET_KEY = SECRET_KEY  # SECRET_KEY
    JWT_ALGORITHM = 'HS256'
    JWT_VERIFY_EXPIRATION = True,
    JWT_LEEWAY = 0
    JWT_EXPIRATION_DELTA = timedelta(seconds=3600 * 24 * 30)
    JWT_AUTH_HEADER_KEY = 'Authorization'
    JWT_AUTH_HEADER_PREFIX = 'Bearer'

    # Register expiration
    REGISTER_EXPIRATION = 3600 * 3

    # Reset Password
    RESET_PWD_EXPIRATION = 3600 * 3

    # redis keys
    INVALID_USER_TOKEN_PREFIX = 'invalid_user_token:'
    RATE_LIMIT_PREFIX = 'rate_limit:'

    # DATABASES
    MONGODB_HOST_ENV = 'localhost'
    if os.environ.get('MONGO_PORT_27017_TCP_ADDR') is not None:
        MONGODB_HOST_ENV = os.environ.get('MONGO_PORT_27017_TCP_ADDR')

    MONGODB_PORT_ENV = 27017
    if os.environ.get('MONGO_PORT_27017_TCP_PORT') is not None:
        MONGODB_PORT_ENV = int(os.environ.get('MONGO_PORT_27017_TCP_PORT'))

    REDIS_HOST_ENV = '127.0.0.1'
    if os.environ.get('REDIS_PORT_6379_TCP_ADDR') is not None:
        REDIS_HOST_ENV = os.environ.get('REDIS_PORT_6379_TCP_ADDR')

    REDIS_PORT_ENV = 6379
    if os.environ.get('REDIS_PORT_6379_TCP_PORT') is not None:
        REDIS_PORT_ENV = int(os.environ.get('REDIS_PORT_6379_TCP_PORT'))

    MONGODB_HOST = MONGODB_HOST_ENV
    MONGODB_PORT = MONGODB_PORT_ENV
    MONGODB_MAX_POOL_SIZE = 10

    # redis
    REDIS_HOST = REDIS_HOST_ENV
    REDIS_PORT = REDIS_PORT_ENV
    REDIS_DB = 0

    # redis
    REDIS_HOST = REDIS_HOST_ENV
    REDIS_PORT = REDIS_PORT_ENV
    REDIS_DB = 0

    # admin
    ADMIN_CODE = unicode(os.environ.get('HYS_ADMIN_CODE', '8261!?'))

    # send mail
    SMTP_HOST = ''
    SMTP_FROM = ''  # send from must same as username.
    SMTP_USERNAME = ''
    SMTP_PASSWORD = ''
    SMTP_TLS = False
    SEND_MAIL = False


class DevelopmentConfig(Config):
    MONGODB_DATABASE = 'hys_dev'

    # cdn
    CDN_USE_SSL = False
    CDN_UPLOADS_BUCKET = 'julolo'
    CDN_ACCOUNT = 'redy.ru@gmail.com'
    CDN_ACCESS_KEY = 'lRXszduxv9_fSvlNbGJa-jn6OVax0FpdnC0J2wQ7'
    CDN_SECRET_KEY = 'MBU2kNmmlLrxGjgf1oZsdt_utOrRNYYuLVOJEA35'

    # urls
    RES_URL = 'http://oy92a9okc.bkt.clouddn.com'
    REFERRER_URL = 'https://servicewechat.com'


class TestCaseConfig(Config):
    UNITTEST = True
    SECRET_KEY = 'secret'
    MONGODB_DATABASE = 'test'


class TestingConfig(Config):
    # cdn
    CDN_USE_SSL = False
    CDN_UPLOADS_BUCKET = 'julolo'
    CDN_ACCOUNT = 'redy.ru@gmail.com'
    CDN_ACCESS_KEY = 'lRXszduxv9_fSvlNbGJa-jn6OVax0FpdnC0J2wQ7'
    CDN_SECRET_KEY = 'MBU2kNmmlLrxGjgf1oZsdt_utOrRNYYuLVOJEA35'

    # urls
    RES_URL = 'http://oy92a9okc.bkt.clouddn.com'
    REFERRER_URL = 'https://servicewechat.com'

    # base
    DENY_PUBLIC_REGISTER = True

    DEPLOY_DIR = '/data/deployment_data/julolo'
    LOG_FOLDER = os.path.join(DEPLOY_DIR, 'log')
    TEMPORARY_FOLDER = os.path.join(DEPLOY_DIR, 'tmp')

    MONGODB_DATABASE = 'julolo'


class ProductionConfig(Config):
    # cdn
    CDN_USE_SSL = False
    CDN_UPLOADS_BUCKET = 'julolo'
    CDN_ACCOUNT = 'redy.ru@gmail.com'
    CDN_ACCESS_KEY = 'WLBKPQs5q58-k7J2n7_uGRKmPfanKsvLRrnsJ7YK'
    CDN_SECRET_KEY = '04kTteV3edbM1nLopFj-xRd0_gs3-rBvmDnaWQzM'

    # urls
    RES_URL = 'http://uploads.julolo.com'
    REFERRER_URL = 'https://servicewechat.com'

    # base
    DEBUG = False
    DENY_PUBLIC_REGISTER = True
    DENY_PUBLIC_ACCESS = True
    SEND_MAIL = True

    DEPLOY_DIR = '/data/deployment_data/julolo'
    LOG_FOLDER = os.path.join(DEPLOY_DIR, 'log')
    TEMPORARY_FOLDER = os.path.join(DEPLOY_DIR, 'tmp')

    # mongodb
    MONGODB_DATABASE = 'julolo'
    MONGODB_USER = None
    MONGODB_PASSWORD = None

    # redis
    REDIS_PASSWORD = None


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'testcase': TestCaseConfig,
    'default': DevelopmentConfig
}
