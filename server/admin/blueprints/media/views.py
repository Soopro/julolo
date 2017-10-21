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

from helpers.media import media_allowed_file, upload_media, del_mediafile

from admin.decorators import login_required


blueprint = Blueprint('media', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    paged = parse_int(request.args.get('paged'), 1, True)

    mediafiles = current_app.mongodb.Media.find_all(True)

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

    if not file or not media_allowed_file(file.filename):
        raise Exception('file type not allowed!')

    upload_media(file)

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
