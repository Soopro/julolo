# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

from utils.misc import uuid4_hex

from helpers.media import media_allowed_file, upload_media

from admin.decorators import login_required

blueprint = Blueprint('category', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    categories = current_app.mongodb.Category.find_all()
    return render_template('cat_list.html', categories=categories)


@blueprint.route('/create')
@login_required
def create():
    category = current_app.mongodb.Category()
    category['slug'] = uuid4_hex(12)
    category.save()

    flash('Created.')
    return_url = url_for('.detail', cat_id=category['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<cat_id>')
@login_required
def detail(cat_id):
    category = current_app.mongodb.Category.find_one_by_id(cat_id)
    return render_template('cat_detail.html', category=category)


@blueprint.route('/detail/<cat_id>', methods=['POST'])
@login_required
def update(cat_id):
    title = request.form['title']
    label = request.form['label']
    caption = request.form['caption']
    icon = request.form['icon']
    poster = request.form['poster']
    cat_ids = request.form['cat_ids']
    priority = request.form['priority']
    status = request.form.get('status')

    category = current_app.mongodb.Category.find_one_by_id(cat_id)
    category['title'] = title
    category['caption'] = caption
    category['icon'] = icon
    category['poster'] = poster
    category['label'] = label or title
    category['cat_ids'] = cat_ids
    category['priority'] = int(priority)
    category['status'] = int(status)
    category.save()

    flash('Saved.')
    return_url = url_for('.detail', cat_id=category['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<cat_id>/remove')
@login_required
def remove(cat_id):
    category = current_app.mongodb.Category.find_one_by_id(cat_id)
    category.delete()
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<cat_id>/upload_icon', methods=['POST'])
@login_required
def upload_icon(cat_id):
    file = request.files['file']
    category = current_app.mongodb.Category.find_one_by_id(cat_id)

    if not category or not file or not media_allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    media = upload_media(file)
    res_url = current_app.config.get('RES_URL')
    category['icon'] = u'{}/{}'.format(res_url, media['key'])
    category.save()

    return_url = url_for('.detail', cat_id=category['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<cat_id>/upload_poster', methods=['POST'])
@login_required
def upload_poster(cat_id):
    file = request.files['file']
    category = current_app.mongodb.Category.find_one_by_id(cat_id)

    if not category or not file or not media_allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    media = upload_media(file)
    res_url = current_app.config.get('RES_URL')
    category['poster'] = u'{}/{}'.format(res_url, media['key'])
    category.save()

    return_url = url_for('.detail', cat_id=category['_id'])
    return redirect(return_url)
