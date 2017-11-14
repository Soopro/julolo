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
def index():
    stores = current_app.mongodb.Store.find_all()
    return render_template('store_list.html', stores=stores)


@blueprint.route('/detail/<store_id>')
@login_required
def detail(store_id):
    store = current_app.mongodb.Store.find_one_by_id(store_id)
    return render_template('store_detail.html', store=store)


@blueprint.route('/create')
@login_required
def create():
    store = current_app.mongodb.Store()
    store['taoke_app_key'] = u''
    store['taoke_app_secret'] = u''
    store['pid'] = u''
    store.save()

    flash('Saved.')
    return_url = url_for('.detail', store_id=store['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<store_id>', methods=['POST'])
@login_required
def update(store_id):
    mini_app_id = request.form['mini_app_id']
    taoke_app_key = request.form['taoke_app_key']
    taoke_app_secret = request.form['taoke_app_secret']
    pid = request.form['pid']
    title = request.form['title']
    splash = request.form['splash']
    tpwd_msg = request.form['tpwd_msg']
    allow_tpwd = request.form.get('allow_tpwd')
    status = request.form.get('status')
    default = request.form.get('default')
    # ssl = request.form.get('ssl')

    if not mini_app_id or \
       not taoke_app_key or \
       not taoke_app_secret or \
       not pid:
        status = 0
    if default:
        current_app.mongodb.Store.freed_default()
    store = current_app.mongodb.Store.find_one_by_id(store_id)
    store['taoke_app_key'] = unicode(taoke_app_key)
    store['taoke_app_secret'] = unicode(taoke_app_secret)
    store['mini_app_id'] = unicode(mini_app_id)
    store['mini_app_secret'] = u''
    store['pid'] = unicode(pid)
    store['title'] = unicode(title)
    store['splash'] = unicode(splash)
    store['allow_tpwd'] = bool(allow_tpwd)
    store['tpwd_msg'] = unicode(tpwd_msg)
    store['ssl'] = False
    store['status'] = parse_int(status)
    store['default'] = bool(default)
    store.save()

    flash('Saved.')
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<store_id>/remove')
@login_required
def remove(store_id):
    store = current_app.mongodb.Store.find_one_by_id(store_id)
    store.delete()
    return render_template('store_detail.html', store=store)
