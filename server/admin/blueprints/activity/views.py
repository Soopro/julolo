# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

from utils.misc import parse_int, process_slug

from helpers.media import media_allowed_file, upload_media

from admin.decorators import login_required

blueprint = Blueprint('activity', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    activities = current_app.mongodb.Activity.find_all()
    return render_template('activity_list.html', activities=activities)


@blueprint.route('/create', methods=['POST'])
@login_required
def create():
    slug = request.form['slug']

    activity = current_app.mongodb.Activity()
    activity['slug'] = process_slug(slug)
    activity.save()

    flash('Created.')
    return_url = url_for('.detail', activity_id=activity['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<activity_id>')
@login_required
def detail(activity_id):
    activity = current_app.mongodb.Activity.find_one_by_id(activity_id)
    return render_template('activity_detail.html', activity=activity)


@blueprint.route('/detail/<activity_id>', methods=['POST'])
@login_required
def update(activity_id):
    title = request.form['title']
    caption = request.form['caption']
    poster = request.form['poster']
    splash = request.form['splash']
    priority = request.form['priority']
    status = request.form.get('status')

    activity = current_app.mongodb.Activity.find_one_by_id(activity_id)
    activity['poster'] = poster
    activity['splash'] = splash
    activity['title'] = title
    activity['caption'] = caption
    activity['priority'] = parse_int(priority)
    activity['status'] = parse_int(status)
    activity.save()

    flash('Saved.')
    return_url = url_for('.detail', activity_id=activity['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<activity_id>/remove')
@login_required
def remove(activity_id):
    activity = current_app.mongodb.Activity.find_one_by_id(activity_id)
    activity.delete()
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/detail/<activity_id>/upload', methods=['POST'])
@login_required
def upload(activity_id):
    file = request.files['file']
    activity = current_app.mongodb.Activity.find_one_by_id(activity_id)

    if not activity or not file or not media_allowed_file(file.filename):
        raise Exception('file upload not allowed!')

    media = upload_media(file)
    res_url = current_app.config.get('RES_URL')
    activity['poster'] = u'{}/{}'.format(res_url, media['key'])
    activity.save()

    return_url = url_for('.detail', activity_id=activity['_id'])
    return redirect(return_url)
