# coding=utf-8
from __future__ import absolute_import


def register_blueprints(app):
    from blueprints.user import blueprint as user_module
    app.register_blueprint(user_module, url_prefix='/user')

    from blueprints.goods import blueprint as goods_module
    app.register_blueprint(goods_module, url_prefix='/goods')
