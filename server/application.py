# coding=utf-8
from __future__ import absolute_import

from flask import Flask, request, current_app
from redis import ConnectionPool, Redis
from mongokit import Connection as MongodbConn

import traceback
import logging

from config import config
from utils.encoders import Encoder
from utils.files import ensure_dirs
from utils.response import make_json_response, make_cors_headers
from apiresps.errors import (NotFound,
                             MethodNotAllowed,
                             BadRequest,
                             UncaughtException)

from common_models import Analyzer
from common_models import (Commodity, Promotion, Category,
                           Tip, Store, Media, Shortcut)


from services.cdn import Qiniu

from envs import CONFIG_NAME
from blueprints import register_blueprints


__version_info__ = ('1', '2', '3')
__version__ = '.'.join(__version_info__)


__maker__ = {
    'creator': ['Redyyu']
}


def create_app(config_name='default'):
    config_name = CONFIG_NAME or config_name

    app = Flask(__name__)

    app.version = __version__
    app.maker = __maker__

    # config
    app.config.from_object(config[config_name])
    app.debug = app.config.get('DEBUG')
    app.json_encoder = Encoder

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

    # inject database connections to app object
    app.redis = rds_conn
    app.mongodb_conn = mongodb_conn
    app.mongodb = mongodb

    # inject analytics
    app.sa_mod = Analyzer(rds_conn, rds_conn)

    # register error handlers
    @app.errorhandler(404)
    def app_error_404(error):
        return make_json_response(NotFound(error))

    @app.errorhandler(405)
    def app_error_405(error):
        return make_json_response(MethodNotAllowed(error))

    @app.errorhandler(400)
    def app_error_400(error):
        return make_json_response(BadRequest(error))

    if app.config.get('UNITTEST') is not True:
        @app.errorhandler(Exception)
        def app_error_uncaught(error):
            current_app.logger.error(
                'Uncaught Exception: {}\n{}'.format(repr(error),
                                                    traceback.format_exc())
            )
            return make_json_response(UncaughtException(error))

    # register before request handlers
    @app.before_request
    def app_before_request():
        # cors response
        if request.method == 'OPTIONS':
            resp = current_app.make_default_options_response()
            cors_headers = make_cors_headers()
            resp.headers.extend(cors_headers)
            return resp

    # register blueprints
    register_blueprints(app)

    print '-------------------------------------------------------'
    print 'Julolo: {}'.format(app.version)
    print 'Creators: {}'.format(', '.join(app.maker['creator']))
    print '-------------------------------------------------------'

    return app
