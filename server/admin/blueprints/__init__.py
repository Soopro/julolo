# coding=utf-8
from __future__ import absolute_import


def register_blueprints(app):
    from admin.blueprints.auth import blueprint as auth_module
    app.register_blueprint(auth_module)

    from admin.blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix='/user')
