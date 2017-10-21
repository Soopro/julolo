# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   render_template)
import os

from utils.model import make_paginator
from utils.misc import parse_int, safe_filename, uuid4_hex

from helpers.media import del_mediafile

from admin.decorators import login_required


blueprint = Blueprint('media', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    paged = parse_int(request.args.get('paged'), 1, True)

    mediafiles = current_app.mongodb.Media.find_all()

    p = make_paginator(mediafiles, paged, 60)

    res_url = current_app.config.get('RES_URL')

    mediafiles = list(mediafiles)

    for media in mediafiles:
        media['src'] = u'{}/{}'.format(res_url, media['key'])

    prev_url = url_for(request.endpoint,
                       paged=p.previous_page)
    next_url = url_for(request.endpoint,
                       paged=p.next_page)

    paginator = {
        'next': next_url if p.has_next else None,
        'prev': prev_url if p.has_previous and p.previous_page else None,
        'paged': p.current_page,
        'start': p.start_index,
        'end': p.end_index,
    }
    return render_template('mediafiles.html',
                           mediafiles=mediafiles,
                           p=paginator)


@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['file']

    if not file or not allowed_file(file.filename):
        raise Exception('file type not allowed!')

    Media = current_app.mongodb.Media

    filename = safe_filename(file.filename)
    key = u'{}/{}'.format('master', filename)

    media = current_app.mongodb.Media.find_one_by_key(key)

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

    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/<media_id>/remove')
@login_required
def remove(media_id):
    paged = parse_int(request.args.get('paged'), 1, True)

    media = current_app.mongodb.Media.find_one_by_id(media_id)
    del_mediafile(media['key'])
    media.delete()

    return_url = url_for('.index', paged=paged)
    return redirect(return_url)


# helpers
def allowed_file(filename):
    file_ext = ''
    allowed_exts = current_app.config.get('ALLOWED_MEDIA_EXTS')
    if '.' in filename:
        file_ext = filename.rsplit('.', 1)[1]
    return file_ext.lower() in allowed_exts
