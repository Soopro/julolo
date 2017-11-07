# coding=utf-8
from __future__ import absolute_import

from flask import Flask, make_response
from redis import ConnectionPool, Redis
from mongokit import Connection as MongodbConn

import traceback
import mimetypes
import logging
from datetime import datetime

from config import config
from utils.encoders import Encoder
from utils.files import ensure_dirs

from common_models import Analyzer
from common_models import (Commodity, Promotion, Category,
                           Tip, Store, Media, Shortcut)

from helpers.media import media_safe_src

from services.cdn import Qiniu
from envs import CONFIG_NAME
from .blueprints import register_blueprints


def create_app(config_name='default'):
    config_name = CONFIG_NAME or config_name

    app = Flask(__name__,
                static_folder='static',
                static_url_path='/static',
                template_folder='templates')

    # config
    app.config.from_object(config[config_name])
    app.debug = app.config.get('DEBUG')
    app.json_encoder = Encoder
    app.jinja_env.cache = None

    ensure_dirs(
        app.config.get('LOG_FOLDER'),
        app.config.get('TEMPORARY_FOLDER')
    )

    # cdn
    app.cdn = Qiniu(
        access_key=app.config.get('CDN_ACCESS_KEY'),
        secret_key=app.config.get('CDN_SECRET_KEY'),
        ssl=app.config.get('CDN_USE_SSL'),
    )

    @app.template_filter()
    def dateformat(t, to_format='%Y-%m-%d'):
        try:
            _date = datetime.fromtimestamp(t)
        except Exception:
            return u''
        return _date.strftime(to_format)

    @app.template_filter()
    def safe_src(url, timestamp=None):
        return media_safe_src(url, timestamp)

    # logging
    if app.config.get('UNITTEST') is True:
        app.logger.setLevel(logging.FATAL)

    # database connections
    rds_pool = ConnectionPool(host=app.config.get('REDIS_HOST'),
                              port=app.config.get('REDIS_PORT'),
                              db=app.config.get('REDIS_DB'),
                              password=app.config.get('REDIS_PASSWORD'))
    rds_conn = Redis(connection_pool=rds_pool)

    mongodb_conn = MongodbConn(
        host=app.config.get('MONGODB_HOST'),
        port=app.config.get('MONGODB_PORT'),
        max_pool_size=app.config.get('MONGODB_MAX_POOL_SIZE')
    )
    mongodb = mongodb_conn[app.config.get('MONGODB_DATABASE')]
    mongodb_user = app.config.get('MONGODB_USER')
    mongodb_pwd = app.config.get('MONGODB_PASSWORD')
    if mongodb_user and mongodb_pwd:
        mongodb.authenticate(mongodb_user, mongodb_pwd)

    # register mongokit models
    mongodb_conn.register([Commodity, Promotion, Category,
                           Tip, Store, Media, Shortcut])

    # register new mimetype
    mimetypes.init()
    mimetypes.add_type('image/svg+xml', '.svg')

    # inject database connections to app object
    app.redis = rds_conn
    app.mongodb_conn = mongodb_conn
    app.mongodb = mongodb

    # inject analytics
    app.sa_mod = Analyzer(rds_conn, rds_conn)

    # register blueprints
    register_blueprints(app)

    # errors
    @app.errorhandler(Exception)
    def errorhandler(err):
        err_detail = traceback.format_exc()
        err_detail = '<br />'.join(err_detail.split('\n'))
        err_msg = '<h1>{}</h1><br/>{}'.format(repr(err), err_detail)
        return make_response(err_msg, 579)

    return app
