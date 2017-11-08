# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

from utils.misc import uuid4_hex, parse_int, process_slug

from helpers.media import media_allowed_file, upload_media

from admin.helpers import helper_list_favorites
from admin.decorators import login_required

blueprint = Blueprint('promotion', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    promotions = current_app.mongodb.Promotion.find_all()
    return render_template('promo_list.html', promotions=promotions)


@blueprint.route('/create')
@login_required
def create():
    promotion = current_app.mongodb.Promotion()
    promotion['slug'] = uuid4_hex(12)
    promotion.save()

    flash('Created.')
    return_url = url_for('.detail', promo_id=promotion['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<promo_id>')
@login_required
def detail(promo_id):
    promotion = current_app.mongodb.Promotion.find_one_by_id(promo_id)
    favorites = helper_list_favorites()
    return render_template('promo_detail.html',
                           promotion=promotion,
                           favorites=favorites)


@blueprint.route('/detail/<promo_id>', methods=['POST'])
@login_required
def update(promo_id):
    title = request.form['title']
    caption = request.form['caption']
    poster = request.form['poster']
    priority = request.form['priority']
    favorite_id = request.form.get('favorite_id')
    favorite_key = request.form.get('favorite_key')
    status = request.form.get('status')

    promotion = current_app.mongodb.Promotion.find_one_by_id(promo_id)
    promotion['poster'] = poster
    promotion['title'] = title
    promotion['caption'] = caption
    promotion['favorite_id'] = parse_int(favorite_id)
    promotion['favorite_key'] = process_slug(favorite_key, False)
    promotion['priority'] = parse_int(priority)
    promotion['status'] = parse_int(status) if favorite_id else 0
    promotion.save()

    flash('Saved.')
    return_url = url_for('.detail', promo_id=promotion['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<promo_id>/remove')
@login_required
def remove(promo_id):
    promotion = current_app.mongodb.Promotion.find_one_by_id(promo_id)
    promotion.delete()
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<promo_id>/upload', methods=['POST'])
@login_required
def upload(promo_id):
    file = request.files['file']
    promotion = current_app.mongodb.Promotion.find_one_by_id(promo_id)

    if not promotion or not file or not media_allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    media = upload_media(file)
    res_url = current_app.config.get('RES_URL')
    promotion['poster'] = u'{}/{}'.format(res_url, media['key'])
    promotion.save()

    return_url = url_for('.detail', promo_id=promotion['_id'])
    return redirect(return_url)
