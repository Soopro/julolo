# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

from utils.misc import uuid4_hex, parse_int

from helpers.media import media_allowed_file, upload_media

from admin.decorators import login_required


blueprint = Blueprint('shortcut', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    shortcuts = current_app.mongodb.Shortcut.find_all()
    return render_template('shortcut_list.html', shortcuts=shortcuts)


@blueprint.route('/create')
@login_required
def create():
    shortcut = current_app.mongodb.Shortcut()
    shortcut['slug'] = uuid4_hex(12)
    shortcut.save()

    flash('Created.')
    return_url = url_for('.detail', shortcut_id=shortcut['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<shortcut_id>')
@login_required
def detail(shortcut_id):
    promotions = list(current_app.mongodb.Promotion.find_all())
    for promo in promotions:
        promo['path'] = u'index/promotion?slug={}'.format(promo['slug'])
    categories = list(current_app.mongodb.Category.find_all())
    for cate in categories:
        cate['path'] = u'index/category?slug={}'.format(cate['slug'])
    shortcut = current_app.mongodb.Shortcut.find_one_by_id(shortcut_id)
    return render_template('shortcut_detail.html',
                           promotions=promotions,
                           categories=categories,
                           shortcut=shortcut)


@blueprint.route('/detail/<shortcut_id>', methods=['POST'])
@login_required
def update(shortcut_id):
    src = request.form['src']
    path = request.form['path']
    priority = request.form['priority']
    status = request.form.get('status')

    shortcut = current_app.mongodb.Shortcut.find_one_by_id(shortcut_id)
    shortcut['src'] = src
    shortcut['path'] = path
    shortcut['priority'] = parse_int(priority)
    shortcut['status'] = parse_int(status) if path else 0
    shortcut.save()

    flash('Saved.')
    return_url = url_for('.detail', shortcut_id=shortcut['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<shortcut_id>/remove')
@login_required
def remove(shortcut_id):
    shortcut = current_app.mongodb.Shortcut.find_one_by_id(shortcut_id)
    shortcut.delete()
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<shortcut_id>/upload', methods=['POST'])
@login_required
def upload(shortcut_id):
    file = request.files['file']
    shortcut = current_app.mongodb.Shortcut.find_one_by_id(shortcut_id)

    if not shortcut or not file or not media_allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    media = upload_media(file)
    res_url = current_app.config.get('RES_URL')
    shortcut['src'] = u'{}/{}'.format(res_url, media['key'])
    shortcut.save()

    return_url = url_for('.detail', shortcut_id=shortcut['_id'])
    return redirect(return_url)
