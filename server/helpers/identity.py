# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request
from bson import ObjectId

from utils.misc import hmac_sha
from utils.auth import (load_token, load_payload)

from apiresps.errors import (Unauthorized,
                             PermissionExpired,
                             PermissionDenied)


def get_current_store():
    referrer_url = current_app.config.get('REFERRER_URL')
    if referrer_url:
        if not request.referrer.startswith(referrer_url):
            raise PermissionDenied('bad referrer')
        ref_path = request.referrer.replace(referrer_url, '').strip('/')
        mini_app_id = ref_path.split('/')[0]
    else:
        mini_app_id = None
    if mini_app_id:
        store = current_app.mongodb.Store.find_one_by_minid(mini_app_id)
    else:
        store = current_app.mongodb.Store.find_one_default()

    if not store:
        raise PermissionDenied('store not found')
    elif current_app.debug:
        print store['title']

    return store


def get_current_user():
    User = current_app.mongodb.User

    token = load_token()
    expired_key_prefix = current_app.config.get('INVALID_USER_TOKEN_PREFIX')
    if current_app.redis.get(expired_key_prefix + token):
        # by user voluntarily exits
        raise PermissionExpired

    payload = load_payload(token)
    try:
        uid = ObjectId(payload['user_id'])
        if not payload.get('sha'):
            raise Exception
    except Exception:
        raise Unauthorized('invalid token')

    user = User.find_one_by_id(uid)

    if user is None:
        raise Unauthorized('not found')
    elif user['status'] == User.STATUS_BANNED:
        raise PermissionDenied('banned')
    elif user['status'] != User.STATUS_ACTIVATED:
        raise PermissionDenied('not activated')

    if _user_hmac_sha(user) != payload['sha']:
        raise Unauthorized('invalid sha')

    return user


# sha
def get_user_hmac_sha(user):
    return _user_hmac_sha(user)


def _user_hmac_sha(user):
    key = u'{}@{}'.format(user['login'], user['password_hash'])
    return hmac_sha(current_app.secret_key, key)
