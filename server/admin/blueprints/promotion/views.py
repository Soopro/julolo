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
    return render_template('promo_detail.html', promotion=promotion)


@blueprint.route('/detail/<promo_id>', methods=['POST'])
@login_required
def update(promo_id):
    title = request.form['title']
    poster = request.form['poster']
    favorite_id = request.form['favorite_id']
    priority = request.form['priority']
    status = request.form.get('status')

    promotion = current_app.mongodb.Promotion.find_one_by_id(promo_id)
    promotion['poster'] = poster
    promotion['title'] = title
    promotion['favorite_id'] = favorite_id
    promotion['priority'] = int(priority)
    promotion['status'] = int(status) if favorite_id else 0
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


@blueprint.route('/detail/<event_id>/upload', methods=['POST'])
@login_required
def upload(org_id):
    file = request.files['file']
    event = current_app.mongodb.Event.find_one_by_id(event_id)

    if not org or not file or not allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    Media = current_app.mongodb.Media

    filename = safe_filename(file.filename)
    key = u'{}/{}'.format('master', filename)

    media = Media.find_one_by_key(key)

    if media:  # rename file if exists.
        fname, ext = os.path.splitext(filename)
        filename = u'{}-{}{}'.format(fname, uuid4_hex(), ext)
        key = u'{}/{}'.format('master', filename)

    mimetype = unicode(file.mimetype)
    size = parse_int(file.content_length)

    file_obj = {
        'filename': filename,
        'stream': file.stream
    }

    bucket = current_app.config.get('CDN_UPLOADS_BUCKET')
    res_url = current_app.config.get('RES_URL')
    src = u'{}/{}'.format(res_url, key)
    try:
        current_app.cdn.upload(bucket, key, file_obj, mimetype)
    except Exception as e:
        raise e

    media = Media()
    media['filename'] = filename
    media['key'] = key
    media['mimetype'] = mimetype
    media['size'] = size
    media.save()

    org['meta']['poster'] = src
    org.save()

    return_url = url_for('.detail', org_id=org['_id'])
    return redirect(return_url)
