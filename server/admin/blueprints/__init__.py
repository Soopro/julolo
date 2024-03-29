# coding=utf-8
from __future__ import absolute_import


def register_blueprints(app):
    from admin.blueprints.dashboard import blueprint as dashboard_module
    app.register_blueprint(dashboard_module)

    from admin.blueprints.auth import blueprint as auth_module
    app.register_blueprint(auth_module, url_prefix='/auth')

    from admin.blueprints.promotion import blueprint as promo_module
    app.register_blueprint(promo_module, url_prefix='/promotion')

    from admin.blueprints.activity import blueprint as activity_module
    app.register_blueprint(activity_module, url_prefix='/activity')

    from admin.blueprints.category import blueprint as cat_module
    app.register_blueprint(cat_module, url_prefix='/category')

    from admin.blueprints.shortcut import blueprint as shortcut_module
    app.register_blueprint(shortcut_module, url_prefix='/shortcut')

    from admin.blueprints.media import blueprint as media_module
    app.register_blueprint(media_module, url_prefix='/media')

    from admin.blueprints.tips import blueprint as tips_module
    app.register_blueprint(tips_module, url_prefix='/tips')

    from admin.blueprints.store import blueprint as store_module
    app.register_blueprint(store_module, url_prefix='/store')

    from admin.blueprints.commodity import blueprint as commodity_module
    app.register_blueprint(commodity_module, url_prefix='/commodity')
