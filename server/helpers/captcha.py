# coding=utf-8
from __future__ import absolute_import

from flask import current_app
from utils.short_url import encode_short_url


def set_captcha(action, key, expires=None, length=6):
    if not isinstance(expires, int):
        expires = 3600
    key = 'captcha-{}-{}'.format(action, key)
    stored_captcha = current_app.redis.get(key)
    if not stored_captcha:
        captcha = encode_short_url(length)
    else:
        captcha = stored_captcha
    current_app.redis.setex(key, captcha, expires)
    return captcha


def check_captcha(action, key, captcha):
    key = 'captcha-{}-{}'.format(action, key)
    stored_captcha = current_app.redis.get(key)
    return stored_captcha and stored_captcha == captcha


def del_captcha(action, key):
    key = 'captcha-{}-{}'.format(action, key)
    current_app.redis.delete(key)
