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

blueprint = Blueprint('event', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    events = current_app.mongodb.Event.find_all()
    events = list(events)

    return render_template('event_list.html', events=events)


@blueprint.route('/create')
@login_required
def create():
    event = current_app.mongodb.Event()
    event['slug'] = uuid4_hex(12)
    event.save()

    flash('Created.')
    return_url = url_for('.detail', event_id=event['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<event_id>')
@login_required
def detail(event_id):
    event = current_app.mongodb.Event.find_one_by_id(event_id)
    return render_template('event_detail.html', event=event)


@blueprint.route('/detail/<event_id>', methods=['POST'])
@login_required
def update(event_id):
    title = request.form['title']
    poster = request.form['poster']
    favorite_id = request.form['favorite_id']
    priority = request.form['priority']
    status = request.form.get('status')

    event = current_app.mongodb.Event.find_one_by_id(event_id)
    event['poster'] = poster
    event['title'] = title
    event['favorite_id'] = unicode(favorite_id)
    event['priority'] = int(priority)
    event['status'] = int(status) if favorite_id else 0
    event.save()

    flash('Saved.')
    return_url = url_for('.detail', event_id=event['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<event_id>/remove')
@login_required
def remove(event_id):
    event = current_app.mongodb.Event.find_one_by_id(event_id)
    event.delete()
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<event_id>/upload', methods=['POST'])
@login_required
def upload(event_id):
    file = request.files['file']
    event = current_app.mongodb.Event.find_one_by_id(event_id)

    if not event or not file or not media_allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    media = upload_media(file)
    res_url = current_app.config.get('RES_URL')
    event['poster'] = u'{}/{}'.format(res_url, media['key'])
    event.save()

    return_url = url_for('.detail', event_id=event['_id'])
    return redirect(return_url)
