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
    categories = current_app.mongodb.Category.find_activated()
    return render_template('store_detail.html',
                           store=store,
                           categories=categories)


@blueprint.route('/create', methods=['POST'])
@login_required
def create():
    mini_app_id = request.form['mini_app_id']

    if current_app.mongodb.Store.find_one_by_minid(mini_app_id):
        raise Exception('mini app_id is duplicated.')

    store = current_app.mongodb.Store()
    store['mini_app_id'] = mini_app_id
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
    sort_type = request.form.get('sort_type')
    top_categories = request.form.getlist('top_categories')
    status = request.form.get('status')
    is_default = request.form.get('default') == 'DEFAULT'
    # ssl = request.form.get('ssl')

    if not pid:
        status = 0

    if is_default:
        current_app.mongodb.Store.freed_default()

    if top_categories:
        cat_ids = u''.join(top_categories)
    else:
        cat_ids = None

    store = current_app.mongodb.Store.find_one_by_id(store_id)
    store['mini_app_id'] = mini_app_id
    store['taoke_app_key'] = taoke_app_key
    store['taoke_app_secret'] = taoke_app_secret
    store['pid'] = pid
    store['title'] = title
    store['splash'] = splash
    store['allow_tpwd'] = bool(allow_tpwd)
    store['tpwd_msg'] = tpwd_msg
    store['ssl'] = False
    store['sort_type'] = parse_int(sort_type)
    store['cat_ids'] = cat_ids
    store['status'] = parse_int(status)
    store['default'] = bool(is_default)
    store.save()

    flash('Saved.')
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<store_id>/remove')
@login_required
def remove(store_id):
    store = current_app.mongodb.Store.find_one_by_id(store_id)
    store.delete()

    flash('Removed.')
    return_url = url_for('.index')
    return redirect(return_url)
