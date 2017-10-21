# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

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
    app_key = request.form['app_key']
    app_secret = request.form['app_secret']
    pid = request.form['pid']
    ssl = request.form.get('ssl')
    allow_tkl = request.form.get('allow_tkl')

    store = current_app.mongodb.Store.find_one()
    if not store:
        store = current_app.mongodb.Store()
    store['app_key'] = unicode(app_key)
    store['app_secret'] = unicode(app_secret)
    store['pid'] = unicode(pid)
    store['ssl'] = bool(ssl)
    store['allow_tkl'] = bool(allow_tkl)
    store.save()

    flash('Saved.')
    return_url = url_for('.settings')
    return redirect(return_url)
