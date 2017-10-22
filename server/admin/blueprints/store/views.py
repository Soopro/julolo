# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

from utils.misc import parse_int

from admin.decorators import login_required

blueprint = Blueprint('store', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def settings():
    store = current_app.mongodb.Store.find_one()
    return render_template('settings.html', store=store)


@blueprint.route('/', methods=['POST'])
@login_required
def update():
    mini_app_id = request.form['mini_app_id']
    taoke_app_key = request.form['taoke_app_key']
    taoke_app_secret = request.form['taoke_app_secret']
    pid = request.form['pid']
    event_limit = request.form['event_limit']
    promo_limit = request.form['promotion_limit']
    cat_ids = request.form['cat_ids']
    tpwd_msg = request.form['tpwd_msg']
    allow_tpwd = request.form.get('allow_tpwd')
    ssl = request.form.get('ssl')

    cat_ids = unicode(cat_ids or u'')
    if len(cat_ids) > 10:
        cat_ids = u''

    event_limit = max(min(parse_int(event_limit, 6, 1), 60), 1)
    promo_limit = max(min(parse_int(promo_limit, 6, 1), 60), 1)

    store = current_app.mongodb.Store.find_one()
    if not store:
        store = current_app.mongodb.Store()
    store['taoke_app_key'] = unicode(taoke_app_key)
    store['taoke_app_secret'] = unicode(taoke_app_secret)
    store['mini_app_id'] = unicode(mini_app_id)
    store['mini_app_secret'] = u''
    store['pid'] = unicode(pid)
    store['cat_ids'] = cat_ids
    store['event_limit'] = event_limit
    store['promotion_limit'] = promo_limit
    store['tpwd_msg'] = unicode(tpwd_msg)
    store['allow_tpwd'] = bool(allow_tpwd)
    store['ssl'] = bool(ssl)
    store.save()

    flash('Saved.')
    return_url = url_for('.settings')
    return redirect(return_url)
