# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.misc import now


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
    if not timestamp:
        timestamp = now()
    try:
        pair = '?' if '?' not in pic_url else '&'
        return u'{}{}t={}'.format(pic_url, pair, timestamp)
    except Exception as e:
        return str(e)
