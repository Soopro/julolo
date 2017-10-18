# coding=utf-8
from __future__ import absolute_import


def register_blueprints(app):
    from blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix='/user')

    from blueprints.store import blueprint as store_module
    app.register_blueprint(store_module, url_prefix='/store')
