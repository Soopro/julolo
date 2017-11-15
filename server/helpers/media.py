# coding=utf-8
from __future__ import absolute_import

from flask import current_app

import os

from utils.misc import now, safe_filename, parse_int, uuid4_hex


def del_mediafile(key):
    bucket = current_app.config.get('CDN_UPLOADS_BUCKET')
    try:
        current_app.cdn.delete(bucket, key)
    except Exception as e:
        current_app.logger.warn(e)


def clean_mediafiles(prefix, recursive=False):
    bucket = current_app.config.get('CDN_UPLOADS_BUCKET')
    try:
        clear = current_app.cdn.clear(bucket, prefix, recursive=recursive)
    except Exception as e:
        current_app.logger.warn(e)
        clear = None
    return clear


def media_safe_src(pic_url, timestamp=None):
    if not pic_url:
        return pic_url
    if not timestamp:
        timestamp = now()
    try:
        pair = '?' if '?' not in pic_url else '&'
        return u'{}{}t={}'.format(pic_url, pair, timestamp)
    except Exception as e:
        return str(e)


def media_safe_splash(pic_url, timestamp=None):
    if not pic_url or not pic_url.startswith(current_app.config['RES_URL']):
        return pic_url
    if not timestamp:
        timestamp = now()
    try:
        pair = '?' if '?' not in pic_url else '&'
        style = 'imageView2/1/w/215/h/168/q/90'
        return u'{}{}t={}&{}'.format(pic_url, pair, timestamp, style)
    except Exception as e:
        return str(e)


def media_allowed_file(filename):
    file_ext = ''
    allowed_exts = current_app.config.get('ALLOWED_MEDIA_EXTS')
    if '.' in filename:
        file_ext = filename.rsplit('.', 1)[1]
    return file_ext.lower() in allowed_exts


def upload_media(file):
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

    return media
