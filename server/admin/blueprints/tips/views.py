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

blueprint = Blueprint('tips', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    tips = current_app.mongodb.Tip.find_all()
    return render_template('tips_list.html', tips=tips)


@blueprint.route('/create')
@login_required
def create():
    tip = current_app.mongodb.Tip()
    tip['key'] = uuid4_hex(12)
    tip.save()

    flash('Created.')
    return_url = url_for('.detail', tip_id=tip['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<tip_id>')
@login_required
def detail(tip_id):
    tip = current_app.mongodb.Tip.find_one_by_id(tip_id)
    return render_template('tip_detail.html', tip=tip)


@blueprint.route('/detail/<tip_id>', methods=['POST'])
@login_required
def update(tip_id):
    title = request.form['title']
    content = request.form['content']
    src = request.form['src']
    priority = request.form['priority']
    status = request.form.get('status')

    tip = current_app.mongodb.Tip.find_one_by_id(tip_id)
    tip['title'] = title
    tip['content'] = content
    tip['src'] = src
    tip['priority'] = int(priority)
    tip['status'] = int(status)
    tip.save()

    flash('Saved.')
    return_url = url_for('.detail', tip_id=tip['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<tip_id>/remove')
@login_required
def remove(tip_id):
    tip = current_app.mongodb.Tip.find_one_by_id(tip_id)
    tip.delete()
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<tip_id>/upload', methods=['POST'])
@login_required
def upload(tip_id):
    file = request.files['file']
    tip = current_app.mongodb.Tip.find_one_by_id(tip_id)

    if not tip or not file or not media_allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    media = upload_media(file)
    res_url = current_app.config.get('RES_URL')
    tip['src'] = u'{}/{}'.format(res_url, media['key'])
    tip.save()

    return_url = url_for('.detail', tip_id=tip['_id'])
    return redirect(return_url)
