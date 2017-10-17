# coding=utf-8
from __future__ import absolute_import

from flask import current_app
from bson import ObjectId

from utils.request import get_remote_addr
from utils.misc import hmac_sha
from utils.auth import (load_token, load_payload)

from apiresps.errors import AuthFailed


def get_current_user():
    User = current_app.mongodb.User

    token = load_token()
    expired_key_prefix = current_app.config.get('INVALID_USER_TOKEN_PREFIX')
    if current_app.redis.get(expired_key_prefix + token):
        raise AuthFailed('token is expired')

    payload = load_payload(token)
    try:
        uid = ObjectId(payload['user_id'])
        if not payload.get('sha'):
            raise Exception
    except Exception:
        raise AuthFailed('invalid token')

    user = User.find_one_by_id(uid)

    if not user:
        raise AuthFailed('not found')
    elif user['status'] != User.STATUS_ACTIVATED:
        raise AuthFailed('not activated')

    if _user_hmac_sha(user) != payload['sha']:
        raise AuthFailed('invalid sha')

    return user


# sha
def get_user_hmac_sha(user):
    return _user_hmac_sha(user)


def _user_hmac_sha(user):
    return hmac_sha(user['login'], user['password_hash'])
